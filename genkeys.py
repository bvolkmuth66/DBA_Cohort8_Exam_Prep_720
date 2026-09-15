import numpy as np, json, math

def excel_var(x):  return float(np.var(x, ddof=1))
def excel_sd(x):   return float(np.std(x, ddof=1))
def excel_cov_s(x,y): return float(np.cov(x,y,ddof=1)[0,1])
def excel_corr(x,y):  return float(np.corrcoef(x,y)[0,1])
def excel_skew(x):
    x=np.asarray(x,float); n=len(x); s=excel_sd(x); m=x.mean()
    return float(n/((n-1)*(n-2))*np.sum(((x-m)/s)**3))
def excel_kurt(x):
    x=np.asarray(x,float); n=len(x); s=excel_sd(x); m=x.mean()
    a=n*(n+1)/((n-1)*(n-2)*(n-3))*np.sum(((x-m)/s)**4)
    b=3*(n-1)**2/((n-2)*(n-3))
    return float(a-b)
def ols(X,y):
    X=np.column_stack([np.ones(len(y))]+[np.asarray(c,float) for c in X])
    b,*_=np.linalg.lstsq(X,np.asarray(y,float),rcond=None)
    yh=X@b; resid=y-yh
    ss_res=float((resid**2).sum()); ss_tot=float(((y-np.mean(y))**2).sum())
    r2=1-ss_res/ss_tot; n=len(y); k=X.shape[1]-1
    adj=1-(1-r2)*(n-1)/(n-k-1)
    return b, r2, adj, resid
def norm_cdf(x): return 0.5*(1+math.erf(x/math.sqrt(2)))
def norm_pdf(x): return math.exp(-x*x/2)/math.sqrt(2*math.pi)
def bs(S,K,r,q,sig,T):
    d1=(math.log(S/K)+(r-q+sig*sig/2)*T)/(sig*math.sqrt(T)); d2=d1-sig*math.sqrt(T)
    c=S*math.exp(-q*T)*norm_cdf(d1)-K*math.exp(-r*T)*norm_cdf(d2)
    p=K*math.exp(-r*T)*norm_cdf(-d2)-S*math.exp(-q*T)*norm_cdf(-d1)
    dc=math.exp(-q*T)*norm_cdf(d1); dp=math.exp(-q*T)*(norm_cdf(d1)-1)
    gam=math.exp(-q*T)*norm_pdf(d1)/(S*sig*math.sqrt(T))
    veg=S*math.exp(-q*T)*norm_pdf(d1)*math.sqrt(T)/100
    thc=(-S*norm_pdf(d1)*sig*math.exp(-q*T)/(2*math.sqrt(T))-r*K*math.exp(-r*T)*norm_cdf(d2)+q*S*math.exp(-q*T)*norm_cdf(d1))/365
    return dict(d1=d1,d2=d2,call=c,put=p,delta_call=dc,delta_put=dp,gamma=gam,vega=veg,theta_call_daily=thc)

K={}

# ---------- Dataset 1 rebuild: low collinearity ----------
rng=np.random.default_rng(2024)
n=30
trust    = np.clip(np.round(rng.normal(4.5,1.45,n)),1,7)
security = np.clip(np.round(0.22*trust + rng.normal(3.5,1.40,n)),1,7)
ease     = np.clip(np.round(0.15*trust + rng.normal(3.9,1.45,n)),1,7)
adopt = np.clip(np.round(0.90+0.42*trust+0.22*security+0.30*ease+rng.normal(0,0.62,n)),1,7)
d1=np.column_stack([trust,security,ease,adopt]).astype(int)
t,s,e,a = [d1[:,i].astype(float) for i in range(4)]
b,r2,adj,_ = ols([t,s,e],a)
vifs=[]
for k_ in range(3):
    others=[d1[:,j].astype(float) for j in range(3) if j!=k_]
    _,r2k,_,_=ols(others,d1[:,k_].astype(float)); vifs.append(1/(1-r2k))
K['dataset1']=dict(
  data=d1.tolist(), n=n,
  means=[round(float(c.mean()),4) for c in (t,s,e,a)],
  sds=[round(excel_sd(c),4) for c in (t,s,e,a)],
  corr_to_dv=[round(excel_corr(c,a),4) for c in (t,s,e)],
  pred_corr=dict(ts=round(excel_corr(t,s),4),te=round(excel_corr(t,e),4),se=round(excel_corr(s,e),4)),
  coef=[round(float(v),4) for v in b], r2=round(r2,4), adj_r2=round(adj,4),
  vif=[round(v,2) for v in vifs])

# ---------- Deriv1: hedging data ----------
rng=np.random.default_rng(23)
dF=np.round(rng.normal(0,0.55,12),2)
dS=np.round(0.86*dF+rng.normal(0,0.20,12),2)
h=excel_cov_s(dS,dF)/excel_var(dF)
K['deriv1']=dict(
  pairs=[[float(a_),float(b_)] for a_,b_ in zip(dS,dF)],
  cov=round(excel_cov_s(dS,dF),6), varF=round(excel_var(dF),6),
  sdS=round(excel_sd(dS),4), sdF=round(excel_sd(dF),4), rho=round(excel_corr(dS,dF),4),
  h=round(h,4), QS=180000, QF=15000, N_exact=round(h*180000/15000,4), N_round=round(h*180000/15000),
  # margin problem: long 2 gold futures, 100 oz, F0=1750, IM 6000/contract, MM 4500/contract
  margin=dict(contracts=2, size=100, F0=1750.0, IM_per=6000.0, MM_per=4500.0,
              total_IM=12000.0, loss_to_call=3000.0, price_drop=15.0, call_price=1735.0),
  mtm_path=[1750,1746,1739,1744,1731,1736])
mp=K['deriv1']['mtm_path']; bal=12000.0; rows=[]
for i in range(1,len(mp)):
    ch=(mp[i]-mp[i-1])*100*2; bal+=ch
    rows.append(dict(day=i,price=mp[i],change=round(ch,2),balance=round(bal,2),
                     call=bal< K['deriv1']['margin']['MM_per']*2))
K['deriv1']['mtm_rows']=rows; K['deriv1']['final_balance']=round(bal,2)
_call=[r for r in rows if r['call']]
K['deriv1']['call_day']=_call[0]['day'] if _call else None
K['deriv1']['call_balance']=_call[0]['balance'] if _call else None
K['deriv1']['variation_margin']=round(12000.0-_call[0]['balance'],2) if _call else None

# ---------- Deriv2: options ----------
p=dict(S=50.0,K=52.0,r=0.05,q=0.0,sig=0.30,T=0.5)
K['deriv2']=dict(params=p, bs={k:round(v,4) for k,v in bs(**p).items()})
# two-step CRR binomial, European call, same params
N=2; dt=p['T']/N; u=math.exp(p['sig']*math.sqrt(dt)); d=1/u
pu=(math.exp((p['r']-p['q'])*dt)-d)/(u-d); disc=math.exp(-p['r']*dt)
ST=[p['S']*u**j*d**(N-j) for j in range(N+1)]
vals=[max(x-p['K'],0) for x in ST]
tree=[[round(v,4) for v in vals]]
while len(vals)>1:
    vals=[disc*(pu*vals[i+1]+(1-pu)*vals[i]) for i in range(len(vals)-1)]
    tree.append([round(v,4) for v in vals])
K['deriv2']['binomial']=dict(N=N,dt=round(dt,6),u=round(u,6),d=round(d,6),p=round(pu,6),
    terminal_S=[round(x,4) for x in ST], call=round(vals[0],4), tree=tree)
pcp=K['deriv2']['bs']['call']+p['K']*math.exp(-p['r']*p['T'])-p['S']
K['deriv2']['pcp_put']=round(pcp,4)

# ---------- Quant1: market model, 36 monthly returns (%) ----------
rng=np.random.default_rng(404)
rm=np.round(rng.normal(0.85,3.90,36),2)
jump=(rng.random(36)<0.14)*rng.normal(0,9.0,36)
shock=rng.normal(0,2.10,36)+jump
rs=np.round(0.30+1.28*rm+shock,2)
b1,r2_1,adj1,res1=ols([rm],rs)
K['quant1']=dict(
  rm=rm.tolist(), rs=rs.tolist(), n=36, rf_monthly=0.30,
  mean_rm=round(float(rm.mean()),4), mean_rs=round(float(rs.mean()),4),
  var_rm=round(excel_var(rm),4), var_rs=round(excel_var(rs),4),
  sd_rm=round(excel_sd(rm),4), sd_rs=round(excel_sd(rs),4),
  skew_rs=round(excel_skew(rs),4), kurt_rs=round(excel_kurt(rs),4),
  skew_rm=round(excel_skew(rm),4), kurt_rm=round(excel_kurt(rm),4),
  cov=round(excel_cov_s(rs,rm),4), corr=round(excel_corr(rs,rm),4),
  alpha=round(float(b1[0]),4), beta=round(float(b1[1]),4),
  beta_check=round(excel_cov_s(rs,rm)/excel_var(rm),4),
  r2=round(r2_1,4))

# ---------- Quant2: portfolio, 4 assets x 36 months ----------
rng=np.random.default_rng(31)
f=rng.normal(0.8,4.0,36)
load=[1.10,0.70,1.30,-0.20]; idio=[3.2,2.4,6.0,1.6]; alp=[0.15,0.25,0.55,0.35]
A=np.round(np.column_stack([alp[i]+load[i]*f+rng.normal(0,idio[i],36) for i in range(4)]),2)
names=["FinTech Equity","Bank Index","Crypto Fund","Bond Fund"]
C=np.cov(A,rowvar=False,ddof=1); mu=A.mean(axis=0)
w=np.array([.25]*4); pv=float(w@C@w); pm=float(w@mu)
i1,i2=1,3
cv=C[i1,i2]; v1,v2=C[i1,i1],C[i2,i2]
wmv=(v2-cv)/(v1+v2-2*cv)
mv_var=wmv**2*v1+(1-wmv)**2*v2+2*wmv*(1-wmv)*cv
rf=0.30
K['quant2']=dict(names=names, data=A.tolist(), n=36, rf=rf,
  means=[round(float(x),4) for x in mu],
  sds=[round(excel_sd(A[:,i]),4) for i in range(4)],
  cov_matrix=[[round(float(C[i][j]),4) for j in range(4)] for i in range(4)],
  corr_matrix=[[round(float(np.corrcoef(A[:,i],A[:,j])[0,1]),4) for j in range(4)] for i in range(4)],
  eq_weight=dict(mean=round(pm,4), var=round(pv,4), sd=round(math.sqrt(pv),4),
                 sharpe=round((pm-rf)/math.sqrt(pv),4),
                 avg_indiv_sd=round(float(np.mean([excel_sd(A[:,i]) for i in range(4)])),4)),
  two_asset=dict(a=names[i1], b=names[i2], w_min_var=round(float(wmv),4),
                 var=round(float(mv_var),4), sd=round(float(math.sqrt(mv_var)),4)))

# ---------- Quant3: event study ----------
rng=np.random.default_rng(1207)
T_est=40; T_evt=5; tot=T_est+T_evt
mkt=np.round(rng.normal(0.04,0.95,tot),3)
true_a,true_b=0.02,1.22
st=np.round(true_a+true_b*mkt+rng.normal(0,0.70,tot),3)
effect=[0.0,0.0,-3.10,-1.55,-0.60]   # event day index 0 within window is day -2
st[T_est:]=np.round(st[T_est:]+np.array(effect),3)
est_m,est_s=mkt[:T_est],st[:T_est]
be,r2e,_,rese=ols([est_m],est_s)
alpha_e,beta_e=float(be[0]),float(be[1])
sd_ar=float(np.std(rese,ddof=2))
ev_days=[-2,-1,0,1,2]
exp_r=[alpha_e+beta_e*mkt[T_est+i] for i in range(T_evt)]
ar=[st[T_est+i]-exp_r[i] for i in range(T_evt)]
car=float(np.sum(ar)); tstat=car/(sd_ar*math.sqrt(T_evt))
K['quant3']=dict(T_est=T_est, T_evt=T_evt, event_days=ev_days,
  est_market=est_m.tolist(), est_stock=est_s.tolist(),
  evt_market=mkt[T_est:].tolist(), evt_stock=st[T_est:].tolist(),
  alpha=round(alpha_e,4), beta=round(beta_e,4), r2=round(r2e,4),
  sd_ar=round(sd_ar,4),
  expected=[round(x,4) for x in exp_r], ar=[round(x,4) for x in ar],
  car=round(car,4), tstat=round(tstat,4),
  significant_5pct=abs(tstat)>1.96)

# ---------- Quant4: Monte Carlo ----------
mc=dict(S0=50.0,K=50.0,r=0.05,q=0.0,sig=0.35,T=1.0,paths=1000)
bench=bs(S=mc['S0'],K=mc['K'],r=mc['r'],q=mc['q'],sig=mc['sig'],T=mc['T'])
rng=np.random.default_rng(5)
z=rng.standard_normal(200000)
ST=mc['S0']*np.exp((mc['r']-0.5*mc['sig']**2)*mc['T']+mc['sig']*math.sqrt(mc['T'])*z)
pay=np.maximum(ST-mc['K'],0)*math.exp(-mc['r']*mc['T'])
K['quant4']=dict(params=mc, bs_call=round(bench['call'],4), bs_put=round(bench['put'],4),
  drift_term=round((mc['r']-0.5*mc['sig']**2)*mc['T'],6),
  diffusion_coef=round(mc['sig']*math.sqrt(mc['T']),6),
  ref_mc_mean=round(float(pay.mean()),4),
  se_1000=round(float(pay.std(ddof=1)/math.sqrt(1000)),4),
  se_10000=round(float(pay.std(ddof=1)/math.sqrt(10000)),4))

json.dump(K, open('keys.json','w'), indent=1)
print("dataset1 R2=%.4f adj=%.4f coef=%s VIF=%s predcorr=%s"%(K['dataset1']['r2'],K['dataset1']['adj_r2'],K['dataset1']['coef'],K['dataset1']['vif'],K['dataset1']['pred_corr']))
print("deriv1 h=%.4f N=%.4f->%d  callprice=%.2f finalbal=%.2f"%(K['deriv1']['h'],K['deriv1']['N_exact'],K['deriv1']['N_round'],K['deriv1']['margin']['call_price'],K['deriv1']['final_balance']))
print("deriv2 call=%.4f put=%.4f delta=%.4f gamma=%.4f vega=%.4f binom=%.4f pcp_put=%.4f"%(K['deriv2']['bs']['call'],K['deriv2']['bs']['put'],K['deriv2']['bs']['delta_call'],K['deriv2']['bs']['gamma'],K['deriv2']['bs']['vega'],K['deriv2']['binomial']['call'],K['deriv2']['pcp_put']))
print("quant1 alpha=%.4f beta=%.4f check=%.4f r2=%.4f skew=%.4f kurt=%.4f"%(K['quant1']['alpha'],K['quant1']['beta'],K['quant1']['beta_check'],K['quant1']['r2'],K['quant1']['skew_rs'],K['quant1']['kurt_rs']))
print("quant2 eq:",K['quant2']['eq_weight'],"twoasset:",K['quant2']['two_asset'])
print("quant3 alpha=%.4f beta=%.4f sdAR=%.4f CAR=%.4f t=%.4f sig=%s"%(K['quant3']['alpha'],K['quant3']['beta'],K['quant3']['sd_ar'],K['quant3']['car'],K['quant3']['tstat'],K['quant3']['significant_5pct']))
print("  AR:",K['quant3']['ar'])
print("quant4 bs=%.4f mcref=%.4f se1000=%.4f"%(K['quant4']['bs_call'],K['quant4']['ref_mc_mean'],K['quant4']['se_1000']))
