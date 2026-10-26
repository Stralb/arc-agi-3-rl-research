"""Dual-headed observational episodic value estimator.
V(s,h) has NO counterfactual action ranking. Q(s,h,a) is a logged-behavior
return predictor, used only as a bounded action-ranking prior, not an oracle.
"""
from __future__ import annotations
import numpy as np
import torch
from torch import nn
from episodic_features import STATE_DIM,ACTION_DIM

class EpisodicValueNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder=nn.Sequential(nn.Linear(STATE_DIM,64),nn.ReLU(),
                                   nn.Linear(64,32),nn.ReLU())
        self.vhead=nn.Sequential(nn.Linear(32,1),nn.Sigmoid())
        self.qhead=nn.Sequential(nn.Linear(32+ACTION_DIM,48),nn.ReLU(),
                                 nn.Linear(48,1),nn.Sigmoid())
    def forward(self,s,a):
        z=self.encoder(s)
        v=self.vhead(z).squeeze(-1)
        q=self.qhead(torch.cat((z,a),-1)).squeeze(-1)
        return v,q

def predict_batched(model,states,actions):
    with torch.inference_mode():
        s=torch.from_numpy(np.asarray(states,np.float32))
        a=torch.from_numpy(np.asarray(actions,np.float32))
        v,q=model(s,a)
        return v.numpy().copy(),q.numpy().copy()