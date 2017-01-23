/*  Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing,
    software distributed under the License is distributed on an
    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
    KIND, either express or implied.  See the License for the
    specific language governing permissions and limitations
    under the License.

    Authors: Shamal Faily 
    Based on Lars Kotthoff's 'Chernoff faces for D3' Block: http://bl.ocks.org/larskotthoff/2011590
*/

function sign(num) {
  if(num > 0) {
    return 1;
  } else if(num < 0) {
    return -1;
  } else {
    return 0;
  }
}

function scale(v,f) {
  return parseFloat((f/60) * v);
} 

function d3_chernoff() {
  var facef = 0, // 0 - 1
      mouthf = 0, // -1 - 1
      eyehf = 0.5, // 0 - 1
      eyewf = 0.5, // 0 - 1
      browf = 0, // -1 - 1
      xf = 0,
      yf = 0,
      frf = 0,

      line = d3.svg.line()
        .interpolate("cardinal-closed")
        .x(function(d) { return d.x; })
        .y(function(d) { return d.y; }),
      bline = d3.svg.line()
        .interpolate("basis-closed")
        .x(function(d) { return d.x; })
        .y(function(d) { return d.y; });

  function chernoff(a) {
    if(a instanceof Array) {
      a.each(__chernoff);
    } else {
      d3.select(this).each(__chernoff);
    }
  }

  function __chernoff(d) {
    var ele = d3.select(this),
      xCoord = parseFloat(typeof(xf) === "function" ? xf(d) : xf),
      yCoord = parseFloat(typeof(yf) === "function" ? yf(d) : yf),
      fRad = parseFloat(typeof(frf) === "function" ? frf(d) : frf),
      mouthvar = parseFloat(typeof(mouthf) === "function" ? mouthf(d) : mouthf) * 7,
      nosehvar = 5,
      nosewvar = 5,
      eyehvar = parseFloat(typeof(eyehf) === "function" ? eyehf(d) : eyehf) * 10,
      eyewvar = parseFloat(typeof(eyewf) === "function" ? eyewf(d) : eyewf) * 10,
      browvar = parseFloat(typeof(browf) === "function" ? browf(d) : browf) * 3;

    var face = d.face;
    ele.selectAll("path.face").data([face]).enter()
       .append("svg:ellipse")
       .attr("class", "face")
       .attr("fill","none")
       .attr("stroke","black")
       .attr("cx", xCoord)
       .attr("cy", yCoord)
       .attr("rx", fRad)
       .attr("ry", fRad);

    var mouth = [{x: parseFloat(xCoord), y: parseFloat(yCoord + scale(15 + mouthvar,fRad))}, //y+15
                 {x: parseFloat(xCoord + scale(40,fRad)), y: parseFloat(yCoord + scale(20 - mouthvar,fRad))}, //x+40,y+20
                 {x: parseFloat(xCoord), y: parseFloat(yCoord + scale(25 + mouthvar,fRad))}, //y+25
                 {x: parseFloat(xCoord - scale(40,fRad)), y: parseFloat(yCoord + scale(15 - mouthvar,fRad))}]; //x-40,y+15
    ele.selectAll("path.mouth").data([mouth]).enter()
       .append("svg:path")
       .attr("class", "mouth")
       .attr("fill","none")
       .attr("stroke","black")
       .attr("d", line); 

    var nose = [{x: parseFloat(xCoord + scale(nosewvar,fRad)), y: parseFloat(yCoord - scale(10 - nosehvar,fRad))},
                {x: parseFloat(xCoord), y: parseFloat(yCoord - scale(10 + nosehvar,fRad))},
                {x: parseFloat(xCoord - scale(nosewvar,fRad)), y: parseFloat(yCoord - scale(10 - nosehvar,fRad))}];
    ele.selectAll("path.nose").data([nose]).enter()
       .append("svg:path")
       .attr("class", "nose")
       .attr("fill","none")
       .attr("stroke","black")
       .attr("d", line);

    var leye = [{x: parseFloat(xCoord - scale(15,fRad)), y: parseFloat(yCoord - scale(25 - eyehvar,fRad))}, {x: parseFloat(xCoord - scale(15 + eyewvar,fRad)), y: parseFloat(yCoord - scale(25,fRad))},
                {x: parseFloat(xCoord - scale(15,fRad)), y: parseFloat(yCoord - scale(25 + eyehvar,fRad))}, {x: parseFloat(xCoord - scale(15 - eyewvar,fRad)), y: parseFloat(yCoord - scale(25,fRad))}];
    var reye = [{x: parseFloat(xCoord + scale(15,fRad)), y: parseFloat(yCoord - scale(25 - eyehvar,fRad))}, {x: parseFloat(xCoord + scale(15 + eyewvar,fRad)), y: parseFloat(yCoord - scale(25,fRad))},
                {x: parseFloat(xCoord + scale(15,fRad)), y: parseFloat(yCoord - scale(25 + eyehvar,fRad))}, {x: parseFloat(xCoord + scale(15 - eyewvar,fRad)), y: parseFloat(yCoord - scale(25,fRad))}];
    ele.selectAll("path.leye").data([leye]).enter()
       .append("svg:path")
       .attr("class", "leye")
       .attr("fill","none")
       .attr("stroke","black")
       .attr("d", bline); 
    ele.selectAll("path.reye").data([reye]).enter()
       .append("svg:path")
       .attr("class", "reye")
       .attr("fill","none")
       .attr("stroke","black")
       .attr("d", bline);

    ele.append("svg:path")
       .attr("class", "lbrow")
       .attr("fill","none")
       .attr("stroke","black")
       .attr("d", "M" + (parseFloat(xCoord - scale(15 - eyewvar/1.7 - sign(browvar),fRad))) + "," +
                        (parseFloat(yCoord - scale(60 - eyehvar + browvar,fRad))) + " " +
                        (parseFloat(xCoord - scale(15 + eyewvar/1.7 - sign(browvar),fRad))) + "," +
                        (parseFloat(yCoord - scale(60 - eyehvar - browvar,fRad))));
    ele.append("svg:path")
       .attr("class", "rbrow")
       .attr("fill","none")
       .attr("stroke","black")
       .attr("d", "M" + (parseFloat(xCoord + scale(15 - eyewvar/1.7+ sign(browvar),fRad))) + "," +
                        (parseFloat(yCoord - scale(60 - eyehvar + browvar,fRad))) + " " +
                        (parseFloat(xCoord + scale(15 + eyewvar/1.7 + sign(browvar),fRad))) + "," +
                        (parseFloat(yCoord - scale(60 - eyehvar - browvar,fRad)))); 
  }

  chernoff.xloc = function(x) {
    if(!arguments.length) return xf;
    xf = x;
    return chernoff;
  };

  chernoff.yloc = function(x) {
    if(!arguments.length) return yf;
    yf = x;
    return chernoff;
  };

  chernoff.frad = function(x) {
    if(!arguments.length) return frf;
    frf = x;
    return chernoff;
  };

  chernoff.mouth = function(x) {
    if(!arguments.length) return mouthf;
    mouthf = x;
    return chernoff;
  };

  chernoff.eyeh = function(x) {
    if(!arguments.length) return eyehf;
    eyehf = x;
    return chernoff;
  };

  chernoff.eyew = function(x) {
    if(!arguments.length) return eyewf;
    eyewf = x;
    return chernoff;
  };

  chernoff.brow = function(x) {
    if(!arguments.length) return browf;
    browf = x;
    return chernoff;
  };

  return chernoff;
}

d3.chernoff = function() {
  return d3_chernoff(Object);
};
