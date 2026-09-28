"""Inspect publicly downloaded benchmark components and write a compact inventory."""
from __future__ import annotations

import csv
import json
from pathlib import Path
import zipfile

import numpy as np
from scipy.io import loadmat


def _obj_vertices(path: Path) -> np.ndarray:
    pts=[]
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("v "):
                parts=line.split()
                if len(parts)>=4:
                    pts.append([float(parts[1]),float(parts[2]),float(parts[3])])
    return np.asarray(pts, dtype=float)


def _legacy_vtk_points(path: Path) -> np.ndarray:
    text=path.read_text(encoding="utf-8", errors="ignore").splitlines()
    for i,line in enumerate(text):
        parts=line.strip().split()
        if len(parts)>=3 and parts[0].upper()=="POINTS":
            n=int(parts[1])
            values=[]
            j=i+1
            while j<len(text) and len(values)<n*3:
                values.extend(float(x) for x in text[j].split())
                j+=1
            if len(values)<n*3:
                raise ValueError(f"VTK POINTS truncated: {path}")
            return np.asarray(values[:n*3],dtype=float).reshape(n,3)
    raise ValueError(f"POINTS block not found: {path}")


def _mesh_summary(path: Path) -> dict:
    if path.suffix.lower()==".obj":
        pts=_obj_vertices(path)
    elif path.suffix.lower()==".vtk":
        pts=_legacy_vtk_points(path)
    else:
        raise ValueError(path)
    if len(pts)==0:
        raise ValueError(f"No vertices: {path}")
    return {
        "path":str(path),
        "vertices":int(len(pts)),
        "min":pts.min(axis=0).tolist(),
        "max":pts.max(axis=0).tolist(),
        "centroid":pts.mean(axis=0).tolist(),
        "extent":(pts.max(axis=0)-pts.min(axis=0)).tolist(),
    }


def _text_preview(path: Path, max_chars=1200):
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:max_chars]
    except Exception:
        return None


def _mat_summary(path: Path) -> dict:
    data=loadmat(path)
    variables={}
    for key,value in data.items():
        if key.startswith("__"):
            continue
        arr=np.asarray(value)
        item={"shape":list(arr.shape),"dtype":str(arr.dtype)}
        if np.issubdtype(arr.dtype, np.number) and arr.size:
            flat=arr.astype(float)
            item["min"]=float(np.nanmin(flat))
            item["max"]=float(np.nanmax(flat))
            item["mean"]=float(np.nanmean(flat))
            if arr.size <= 100:
                item["values"]=arr.tolist()
        variables[key]=item
    return {"path":str(path),"variables":variables}


def inspect_jaw(root: Path) -> dict:
    files=[p for p in root.rglob("*") if p.is_file()]
    items=[]
    mats=[]
    for p in files:
        item={"path":str(p.relative_to(root)),"size_bytes":p.stat().st_size}
        if p.suffix.lower() in {".txt",".csv",".tsv",".md",".json"}:
            item["preview"]=_text_preview(p)
        if p.suffix.lower()==".mat" and len(mats)<8:
            mats.append(_mat_summary(p))
        items.append(item)
    return {"file_count":len(files),"files":items[:100],"mat_samples":mats}


def inspect_face(root: Path) -> dict:
    files=[p for p in root.rglob("*") if p.is_file()]
    objs=[p for p in files if p.suffix.lower()==".obj"]
    bins=[p for p in files if p.suffix.lower()==".bin"]
    transforms=[p for p in files if p.name.endswith("_transform.txt")]
    out={
        "file_count":len(files),
        "obj_count":len(objs),
        "bin_count":len(bins),
        "headpose_transform_count":len(transforms),
        "sample_files":[str(p.relative_to(root)) for p in files[:30]],
    }
    if objs:
        out["first_obj"]=_mesh_summary(objs[0])
    if transforms:
        out["first_headpose_path"]=str(transforms[0].relative_to(root))
        out["first_headpose_preview"]=_text_preview(transforms[0])
    return out


def main():
    root=Path("online_case")
    report={
        "benchmark_label":"composite public-data engineering benchmark; not patient-specific",
        "dental":{
            "lower":_mesh_summary(root/"dental"/"0EJBIPTC_lower.obj"),
            "upper":_mesh_summary(root/"dental"/"0EJBIPTC_upper.vtk"),
            "source_case_id":"0EJBIPTC",
        },
        "jaw":inspect_jaw(root/"jaw"),
        "face":inspect_face(root/"face"),
    }
    Path("online_case/inventory.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))


if __name__=="__main__":
    main()
