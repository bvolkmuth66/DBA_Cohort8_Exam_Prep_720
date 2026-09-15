/* DBA 720 Practice Lab - shared helpers (v3.0)
   Tolerance-based grading, Excel-exact statistics, CSV export. */
var Lab=(function(){
  function $(id){return document.getElementById(id);}
  function val(id){var e=$(id);return e?e.value:"";}
  function num(id){var v=parseFloat(val(id));return isNaN(v)?null:v;}
  function chk(id){var e=$(id);return e?e.checked:false;}

  /* ---------- Excel-equivalent statistics ---------- */
  function mean(a){return a.reduce(function(s,x){return s+x;},0)/a.length;}
  function varS(a){var m=mean(a);return a.reduce(function(s,x){return s+(x-m)*(x-m);},0)/(a.length-1);}
  function sdS(a){return Math.sqrt(varS(a));}
  function covS(a,b){var ma=mean(a),mb=mean(b),s=0;
    for(var i=0;i<a.length;i++)s+=(a[i]-ma)*(b[i]-mb);return s/(a.length-1);}
  function corr(a,b){return covS(a,b)/(sdS(a)*sdS(b));}
  function skew(a){var n=a.length,m=mean(a),s=sdS(a),t=0;
    for(var i=0;i<n;i++)t+=Math.pow((a[i]-m)/s,3);
    return n/((n-1)*(n-2))*t;}
  function kurt(a){var n=a.length,m=mean(a),s=sdS(a),t=0;
    for(var i=0;i<n;i++)t+=Math.pow((a[i]-m)/s,4);
    return n*(n+1)/((n-1)*(n-2)*(n-3))*t - 3*(n-1)*(n-1)/((n-2)*(n-3));}
  function slope(y,x){return covS(y,x)/varS(x);}      /* Excel SLOPE   */
  function intercept(y,x){return mean(y)-slope(y,x)*mean(x);} /* Excel INTERCEPT */
  function rsq(y,x){var r=corr(y,x);return r*r;}      /* Excel RSQ     */
  function col(rows,j){return rows.map(function(r){return r[j];});}

  /* ---------- grading ---------- */
  function near(a,e,tol){return a!==null&&Math.abs(a-e)<=tol;}
  /* items: {id,label,expected,tol}  or {id,label,is:"value",type:"select"|"checkbox"} */
  function gradeItems(items){
    var lines=[],score=0;
    items.forEach(function(it){
      var ok,got;
      if(it.type==="select"){got=val(it.id);ok=(got===it.is);}
      else if(it.type==="checkbox"){got=chk(it.id)?"checked":"unchecked";ok=(chk(it.id)===it.is);}
      else if(it.type==="set"){ok=it.ids.every(function(x,i){return chk(x)===it.want[i];});got="";}
      else {got=num(it.id);ok=near(got,it.expected,it.tol);}
      if(ok)score++;
      var shown=(it.type||"number")==="number"
        ? (got===null?"(blank)":got)+(ok?"":" \u2192 expected "+it.expected)
        : (ok?"correct":"not correct");
      lines.push('<li class="'+(ok?"itemok":"itembad")+'">'+it.label+": "+shown+"</li>");
    });
    return {score:score,total:items.length,html:lines.join("")};
  }
  function report(elId,res,passPct,onPass){
    var pct=Math.round(res.score/res.total*100);
    var good=pct>=(passPct||80);
    $(elId).innerHTML='<div class="result '+(good?"good":"poor")+'">'+
      '<strong>Score: '+pct+'%</strong> ('+res.score+' of '+res.total+')'+
      '<ul>'+res.html+'</ul></div>';
    if(good&&onPass)onPass();
    return good;
  }

  /* ---------- rendering ---------- */
  function renderTable(elId,cols,rows,rowLabels){
    var h='<div class="scroll"><table><thead><tr>';
    if(rowLabels)h+='<th class="lbl">#</th>';
    cols.forEach(function(c){h+="<th>"+c+"</th>";});
    h+="</tr></thead><tbody>";
    rows.forEach(function(r,i){
      h+="<tr>";
      if(rowLabels)h+='<td class="lbl">'+(rowLabels[i]!==undefined?rowLabels[i]:i+1)+"</td>";
      r.forEach(function(v){h+="<td>"+v+"</td>";});
      h+="</tr>";
    });
    return ($(elId).innerHTML=h+"</tbody></table></div>");
  }
  function exportCSV(name,cols,rows){
    var csv=cols.join(",")+"\n"+rows.map(function(r){return r.join(",");}).join("\n");
    var a=document.createElement("a");
    a.href=URL.createObjectURL(new Blob([csv],{type:"text/csv"}));
    a.download=name;document.body.appendChild(a);a.click();document.body.removeChild(a);
  }
  function show(id){$(id).classList.remove("hidden");$(id).scrollIntoView({behavior:"smooth",block:"start"});}
  function reveal(id){$(id).classList.remove("hidden");}
  function fmt(x,d){return Number(x).toFixed(d===undefined?4:d);}

  return {$:$,val:val,num:num,chk:chk,mean:mean,varS:varS,sdS:sdS,covS:covS,corr:corr,
          skew:skew,kurt:kurt,slope:slope,intercept:intercept,rsq:rsq,col:col,
          near:near,gradeItems:gradeItems,report:report,renderTable:renderTable,
          exportCSV:exportCSV,show:show,reveal:reveal,fmt:fmt};
})();
