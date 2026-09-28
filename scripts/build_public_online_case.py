"""Build the first executable public online-data 4D dental engineering case.

This script intentionally keeps dental, face, and jaw source identities separate.
It produces a dental-motion visualization using the public dental sample and a
real Figshare engineering trajectory, while reporting MultiFace motion metadata
as an independent facial-motion module. It is NOT a patient-specific digital twin.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
from scipy.io import loadmat


ROOT = Path("online_case")
OUT = ROOT / "output"


def load_obj_vertices(path: Path) -> np.ndarray:
    pts=[]
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("v "):
                p=line.split()
                if len(p)>=4:
                    pts.append([float(p[1]),float(p[2]),float(p[3])])
    if not pts:
        raise ValueError(f"No OBJ vertices in {path}")
    return np.asarray(pts,float)


def load_vtk_points(path: Path) -> np.ndarray:
    lines=path.read_text(encoding="utf-8",errors="ignore").splitlines()
    for i,line in enumerate(lines):
        p=line.strip().split()
        if len(p)>=3 and p[0].upper()=="POINTS":
            n=int(p[1])
            vals=[]
            j=i+1
            while j<len(lines) and len(vals)<n*3:
                vals.extend(float(x) for x in lines[j].split())
                j+=1
            if len(vals)<n*3:
                raise ValueError(f"Truncated VTK points in {path}")
            return np.asarray(vals[:n*3],float).reshape(n,3)
    raise ValueError(f"No VTK POINTS block in {path}")


def load_reference_jaw_curve(path: Path) -> tuple[np.ndarray,str]:
    data=loadmat(path)
    keys=[k for k in data if not k.startswith("__")]
    if len(keys)!=1:
        raise ValueError(f"Expected one trajectory variable in {path}; got {keys}")
    key=keys[0]
    arr=np.asarray(data[key],float)
    if arr.ndim!=2 or arr.shape[1]!=3:
        raise ValueError(f"Expected Nx3 trajectory in {path}; got {arr.shape}")
    return arr,key


def resample_xyz(points: np.ndarray, n: int) -> np.ndarray:
    old=np.linspace(0.0,1.0,len(points))
    new=np.linspace(0.0,1.0,n)
    return np.column_stack([np.interp(new,old,points[:,i]) for i in range(3)])


def load_multiface_headposes(face_root: Path) -> list[tuple[str,np.ndarray]]:
    files=sorted(face_root.rglob("*_transform.txt"), key=lambda p: int(p.name.split("_")[0]))
    out=[]
    for p in files:
        m=np.loadtxt(p)
        if m.shape==(3,4):
            T=np.eye(4)
            T[:3,:]=m
        elif m.shape==(4,4):
            T=m
        else:
            raise ValueError(f"Unexpected headpose shape {m.shape}: {p}")
        out.append((p.name,T))
    if not out:
        raise ValueError("No MultiFace head-pose transforms found")
    return out


def rotation_angle_deg(R: np.ndarray) -> float:
    v=float(np.clip((np.trace(R)-1.0)/2.0,-1.0,1.0))
    return math.degrees(math.acos(v))


def face_motion_summary(poses: list[tuple[str,np.ndarray]]) -> dict:
    T0=poses[0][1]
    inv0=np.linalg.inv(T0)
    translations=[]
    rotations=[]
    for _,T in poses:
        rel=T @ inv0
        translations.append(rel[:3,3])
        rotations.append(rotation_angle_deg(rel[:3,:3]))
    xyz=np.asarray(translations)
    step=np.linalg.norm(np.diff(xyz,axis=0),axis=1) if len(xyz)>1 else np.array([])
    return {
        "frames":len(poses),
        "first_frame":poses[0][0],
        "last_frame":poses[-1][0],
        "relative_translation_path_units":float(step.sum()) if len(step) else 0.0,
        "max_relative_translation_units":float(np.linalg.norm(xyz,axis=1).max()),
        "max_relative_rotation_deg":float(max(rotations)),
        "note":"MultiFace head-pose units/convention retained as published; not spatially registered to dental anatomy in this benchmark stage."
    }


def choose_display_axis(upper: np.ndarray, lower: np.ndarray) -> int:
    ext=(np.ptp(upper,axis=0)+np.ptp(lower,axis=0))/2.0
    return int(np.argmin(ext))


def standardize_dental_pair(upper: np.ndarray, lower: np.ndarray) -> tuple[np.ndarray,np.ndarray,int]:
    # The public challenge meshes are independently normalized. We therefore
    # center each arch independently and add an explicit display-only separation.
    uc=upper-upper.mean(axis=0)
    lc=lower-lower.mean(axis=0)
    axis=choose_display_axis(uc,lc)
    separation_mm=36.0
    uoff=np.zeros(3); loff=np.zeros(3)
    uoff[axis]=separation_mm/2.0
    loff[axis]=-separation_mm/2.0
    return uc+uoff,lc+loff,axis


def sample_points(x: np.ndarray, max_points=2500) -> np.ndarray:
    if len(x)<=max_points:
        return x
    idx=np.linspace(0,len(x)-1,max_points,dtype=int)
    return x[idx]


def render_gif(upper: np.ndarray, lower: np.ndarray, jaw: np.ndarray, path: Path) -> None:
    up=sample_points(upper)
    low=sample_points(lower)
    allpts=np.vstack([up, low + jaw[np.argmax(np.linalg.norm(jaw,axis=1))]])
    mins=allpts.min(axis=0)-5
    maxs=allpts.max(axis=0)+5

    fig=plt.figure(figsize=(7,7))
    ax=fig.add_subplot(111,projection="3d")
    upper_sc=ax.scatter(up[:,0],up[:,1],up[:,2],s=1,label="Public upper arch")
    lower_sc=ax.scatter(low[:,0],low[:,1],low[:,2],s=1,label="Public lower arch")
    ax.set_xlim(mins[0],maxs[0]); ax.set_ylim(mins[1],maxs[1]); ax.set_zlim(mins[2],maxs[2])
    ax.set_xlabel("X (mm)"); ax.set_ylabel("Y (mm)"); ax.set_zlabel("Z (mm)")
    ax.set_title("Composite public-data dental motion benchmark")
    ax.legend(loc="upper right")

    def update(i):
        moved=low+jaw[i]
        lower_sc._offsets3d=(moved[:,0],moved[:,1],moved[:,2])
        ax.set_title(f"Composite public-data dental motion — frame {i+1}/{len(jaw)}")
        return (upper_sc,lower_sc)

    ani=FuncAnimation(fig,update,frames=len(jaw),interval=1000/20,blit=False)
    ani.save(path,writer=PillowWriter(fps=20))
    plt.close(fig)


def save_standard_motion(jaw: np.ndarray, path: Path) -> None:
    fields=["frame_index","tx_mm","ty_mm","tz_mm","qw","qx","qy","qz","jaw_opening_mm"]
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader()
        for i,p in enumerate(jaw):
            w.writerow({
                "frame_index":i,
                "tx_mm":float(p[0]),
                "ty_mm":float(p[1]),
                "tz_mm":float(p[2]),
                "qw":1.0,"qx":0.0,"qy":0.0,"qz":0.0,
                "jaw_opening_mm":"",
            })


def main():
    OUT.mkdir(parents=True,exist_ok=True)

    lower=load_obj_vertices(ROOT/"dental"/"0EJBIPTC_lower.obj")
    upper=load_vtk_points(ROOT/"dental"/"0EJBIPTC_upper.vtk")
    upper_display,lower_display,separation_axis=standardize_dental_pair(upper,lower)

    jaw_raw,jaw_variable=load_reference_jaw_curve(
        ROOT/"jaw"/"unpacked"/"Position Datasets"/"KREIVES"/"KKre1.mat"
    )
    # Reference positioning trajectory in millimetre-scale coordinates.
    jaw_relative=jaw_raw-jaw_raw[0]

    poses=load_multiface_headposes(ROOT/"face")
    jaw=resample_xyz(jaw_relative,len(poses))

    steps=np.linalg.norm(np.diff(jaw,axis=0),axis=1)
    disp=np.linalg.norm(jaw,axis=1)

    save_standard_motion(jaw,OUT/"jaw_motion_from_figshare.csv")
    render_gif(upper_display,lower_display,jaw,OUT/"public_online_dental_motion.gif")

    metrics={
        "claim_level":"engineering_benchmark_not_patient_specific",
        "dental":{
            "source":"3DTeethSeg public challenge sample",
            "case_id":"0EJBIPTC",
            "upper_vertices":int(len(upper)),
            "lower_vertices":int(len(lower)),
            "independent_normalization_detected":True,
            "display_only_centroid_separation_mm":36.0,
            "display_separation_axis_index":separation_axis,
            "warning":"The upper/lower public challenge meshes are independently normalized; their display separation is not a patient bite registration."
        },
        "jaw_motion":{
            "source":"Figshare 13397528",
            "source_file":"Position Datasets/KREIVES/KKre1.mat",
            "source_variable":jaw_variable,
            "source_points":int(len(jaw_raw)),
            "render_frames":int(len(jaw)),
            "translation_only":True,
            "path_length_mm_assuming_published_position_units_are_mm":float(steps.sum()),
            "max_displacement_from_start_mm_assuming_published_position_units_are_mm":float(disp.max()),
            "rotation":"not available in selected position trajectory; identity quaternion used",
        },
        "face_motion":face_motion_summary(poses),
    }
    (OUT/"metrics.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8")

    provenance={
        "benchmark":"public-online-composite-v1",
        "claim_level":"engineering_benchmark_not_patient_specific",
        "components":[
            {
                "role":"dental_geometry",
                "dataset":"3DTeethSeg / Teeth3DS challenge public test sample",
                "case_id":"0EJBIPTC",
                "lower_url":"https://github.com/abenhamadou/3DTeethSeg_MICCAI_Challenges",
                "upper_url":"https://github.com/DCBIA-OrthoLab/3DTeethSeg22_challenge",
            },
            {
                "role":"jaw_translation_trajectory",
                "dataset":"Accelerometry-enhanced Magnetic Sensor for Intra-oral Continuous Jaw Motion Tracking and Bruxism Detection",
                "article_id":"13397528",
                "file":"KREIVES/KKre1.mat",
                "url":"https://figshare.com/articles/dataset/Accelerometry-enhanced_Magnetic_Sensor_for_Intra-oral_Continuous_Jaw_Motion_Tracking_and_Bruxism_Detection/13397528",
                "license":"CC BY 4.0",
            },
            {
                "role":"facial_motion_module",
                "dataset":"MultiFace",
                "entity":"6795937",
                "expression":"E061_Lips_Puffed",
                "frames":len(poses),
                "url":"https://github.com/facebookresearch/multiface",
                "license":"CC BY-NC 4.0",
                "note":"Used for independent facial-motion/head-pose module metrics; not anatomically registered to dental geometry in v1.",
            },
        ],
    }
    (OUT/"provenance.json").write_text(json.dumps(provenance,indent=2),encoding="utf-8")

    summary=f"""# Public online composite case v1

This is an engineering benchmark, **not a patient-specific digital twin**.

## Executed public components

- Dental: public case 0EJBIPTC from 3DTeethSeg challenge assets.
- Jaw: Figshare 13397528, KREIVES/KKre1.mat coordinate trajectory.
- Face: MultiFace entity 6795937, E061_Lips_Puffed, {len(poses)} tracked frames.

## Dental-motion output

- Frames: {len(jaw)}
- Jaw source points: {len(jaw_raw)}
- Translation path length (assuming published position units are mm): {steps.sum():.3f} mm
- Maximum translation from start: {disp.max():.3f} mm
- Output GIF: public_online_dental_motion.gif

## Important limitations

1. The public upper and lower challenge meshes are independently normalized; a 36-mm display-only centroid separation is applied.
2. The selected Figshare trajectory provides XYZ position data; rotation is not available in this selected file, so only translation is used.
3. MultiFace is a different public identity and is analyzed as an independent facial-motion module in v1; it is not spatially registered to the dental sample.
4. No patient-specific or clinical digital-twin claim is made.
"""
    (OUT/"SUMMARY.md").write_text(summary,encoding="utf-8")
    print(json.dumps(metrics,indent=2))


if __name__=="__main__":
    main()
