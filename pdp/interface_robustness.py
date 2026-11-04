"""Explicitly scoped coordinate diagnostics; never assigns binding or activation."""
import numpy as np

def rigid_fit(moving,reference):
 moving=np.asarray(moving,dtype=float);reference=np.asarray(reference,dtype=float)
 if moving.shape!=reference.shape or moving.ndim!=2 or moving.shape[1]!=3 or len(moving)<3:raise ValueError('Need matched >=3 xyz points')
 if not np.isfinite(moving).all() or not np.isfinite(reference).all():raise ValueError('Non-finite fit coordinates')
 cm=moving.mean(0);cr=reference.mean(0);u,_,vt=np.linalg.svd((moving-cm).T@(reference-cr));rotation=u@vt
 if np.linalg.det(rotation)<0:u[:,-1]*=-1;rotation=u@vt
 return cm,rotation,cr

def apply_fit(points,fit):
 cm,rotation,cr=fit
 return (np.asarray(points,dtype=float)-cm)@rotation+cr

def rmsd(a,b):
 a=np.asarray(a,dtype=float);b=np.asarray(b,dtype=float)
 if a.shape!=b.shape or a.ndim!=2 or a.shape[1]!=3 or not len(a) or not np.isfinite(a).all() or not np.isfinite(b).all():raise ValueError('Need finite matched nonempty coordinate arrays')
 return float(np.sqrt(np.mean(np.sum((a-b)**2,axis=1))))

def scoped_pose_metrics(reference,prediction,*,target='A',binder='B',target_fit_positions,binder_positions=None,regions=None):
 """Arrays are complete-polymer one-based CA maps (NaN allowed ONLY outside selected positions)."""
 if set(reference)!=set(prediction) or target==binder:raise ValueError('Chain mismatch')
 for c in reference:
  if np.shape(reference[c])!=np.shape(prediction[c]):raise ValueError('Polymer coordinate shape mismatch')
 def get(x,c,positions):
  ps=list(positions)
  if len(ps)!=len(set(ps)) or not ps or min(ps)<1 or max(ps)>len(x[c]):raise ValueError('Invalid/duplicate one-based positions')
  return np.asarray(x[c],dtype=float)[np.asarray(ps)-1]
 ts=list(target_fit_positions);bs=list(binder_positions) if binder_positions is not None else list(range(1,len(reference[binder])+1));fit=rigid_fit(get(prediction,target,ts),get(reference,target,ts));pb=get(prediction,binder,bs);rb=get(reference,binder,bs)
 all_ref=[];all_pred=[]
 for c in sorted(reference):
  r=np.asarray(reference[c],float);p=np.asarray(prediction[c],float);valid=np.isfinite(r).all(1)&np.isfinite(p).all(1);all_ref.extend(r[valid]);all_pred.extend(p[valid])
 gf=rigid_fit(all_pred,all_ref)
 out={'target_fit_CA_count':len(ts),'binder_pose_CA_count':len(bs),'target_fit_CA_RMSD_A':rmsd(apply_fit(get(prediction,target,ts),fit),get(reference,target,ts)),'binder_CA_RMSD_after_target_fit_A':rmsd(apply_fit(pb,fit),rb),'binder_CA_shape_RMSD_after_self_fit_A':rmsd(apply_fit(pb,rigid_fit(pb,rb)),rb),'global_complex_CA_RMSD_A':rmsd(apply_fit(all_pred,gf),all_ref),'regional_CA_RMSD_after_target_fit_A':{},'meaning':'Pose, fold shape, target deformation and remote motion separately. No biological classification.'}
 for name,(c,ps) in (regions or {}).items():out['regional_CA_RMSD_after_target_fit_A'][name]={'CA_count':len(ps),'RMSD_A':rmsd(apply_fit(get(prediction,c,ps),fit),get(reference,c,ps))}
 return out
