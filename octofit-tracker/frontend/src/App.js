import React, {useState as S, useEffect as E} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const U='http://localhost:8000/hub';
const F=(p,c)=>fetch(`${U}/${p}/`).then(r=>r.json()).then(c).catch(()=>{});

const A = ()=>{
  const[v,sV]=S('h'),[k,sK]=S([]),[g,sG]=S([]),[d,sD]=S([]),[p,sP]=S([]),[r,sR]=S([]),[b,sB]=S([]);
  E(()=>{F('k',sK);F('g',sG);F('d',sD);F('p',sP);F('rank',sR);F('bat',x=>sB(x.res||[]));},[]);
  
  return<div className="bg-light min-vh-100">
    <nav className="navbar navbar-dark bg-dark mb-4">
      <div className="container-fluid">
        <span className="navbar-brand">🏃 OctoFit</span>
        <div className="btn-group">
          {['h','r','t','d','p'].map(x=>
            <button key={x} className={`btn btn-sm ${v===x?'btn-primary':'btn-outline-light'}`} onClick={()=>sV(x)}>
              {x.toUpperCase()}
            </button>
          )}
        </div>
      </div>
    </nav>
    <div className="container">
      {v==='h'&&<div className="row g-3">
        <div className="col-md-6"><div className="card bg-primary text-white"><div className="card-body"><h3>{k.length}</h3><p>Athletes</p></div></div></div>
        <div className="col-md-6"><div className="card bg-success text-white"><div className="card-body"><h3>{d.length}</h3><p>Workouts</p></div></div></div>
        <div className="col-md-6"><div className="card bg-warning text-dark"><div className="card-body"><h3>{g.length}</h3><p>Teams</p></div></div></div>
        <div className="col-md-6"><div className="card bg-info text-white"><div className="card-body"><h3>{p.length}</h3><p>Plans</p></div></div></div>
      </div>}
      {v==='r'&&<div className="card">
        <div className="card-header bg-warning"><h4>🏆 Rankings</h4></div>
        <table className="table mb-0">
          <thead><tr><th>Pos</th><th>Name</th><th>Pts</th><th>Streak</th><th>Gr</th><th>Mul</th></tr></thead>
          <tbody>{r.map((x,i)=><tr key={i} className={i<3?'table-warning':''}>
            <td>#{x.p}</td><td>{x.n}</td><td><span className="badge bg-primary">{x.pt}</span></td>
            <td><span className="badge bg-danger">{x.s}🔥</span></td><td>{x.g}</td><td>{x.m}x</td>
          </tr>)}</tbody>
        </table>
      </div>}
      {v==='t'&&<div className="card">
        <div className="card-header bg-success text-white"><h4>👥 Teams</h4></div>
        <table className="table mb-0">
          <thead><tr><th>Rk</th><th>Team</th><th>Pow</th><th>Sz</th><th>Wins</th></tr></thead>
          <tbody>{b.map((x,i)=><tr key={i}>
            <td><span className="badge" style={{backgroundColor:x.c}}>{x.r}</span></td>
            <td><strong>{x.n}</strong></td><td>{x.p}</td><td>{x.s}</td>
            <td><span className="badge bg-success">{x.w}</span></td>
          </tr>)}</tbody>
        </table>
      </div>}
      {v==='d'&&<div className="row">{d.slice(0,12).map((x,i)=>
        <div key={i} className="col-md-4 mb-3">
          <div className="card"><div className="card-body">
            <h6>{x.k?.u?.username||'?'}</h6>
            <p className="mb-1">Type: {x.knd}</p>
            <p className="mb-1">Time: {x.tm}m</p>
            <p className="mb-1">Eff: {x.eff}/10</p>
            <span className="badge bg-info">{x.pts} pts</span>
            {x.nt&&<small className="d-block text-muted mt-2">{x.nt}</small>}
          </div></div>
        </div>
      )}</div>}
      {v==='p'&&<div className="row">{p.map((x,i)=>
        <div key={i} className="col-md-6 mb-3">
          <div className="card">
            <div className={`card-header ${x.tr==='g'?'bg-success':x.tr==='y'?'bg-warning':'bg-danger'} text-white`}>
              <h5>{x.nm}</h5>
            </div>
            <div className="card-body">
              <p>{x.hw}</p>
              <div className="d-flex justify-content-between">
                <span>Time: {x.mn}m</span><span>Focus: {x.fz}</span>
              </div>
              <div className="mt-2">
                <span className="badge bg-primary">{x.lks}❤️</span>
                <span className="badge bg-secondary ms-2">{x.ps}</span>
              </div>
              {x.gr&&<small className="d-block text-muted mt-2">Gear: {x.gr}</small>}
            </div>
          </div>
        </div>
      )}</div>}
    </div>
  </div>;
};

export default A;
