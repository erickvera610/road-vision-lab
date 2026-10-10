const assert=require('node:assert/strict');
const {runEnhanced}=require('./enhanced.js');const r=runEnhanced({noise:10});assert.ok(r.detected);assert.ok(r.synthetic_width_error_px<5);assert.equal(runEnhanced({image:Array.from({length:48},()=>Array(64).fill(0))}).detected,false);assert.throws(()=>runEnhanced({noise:99}));
console.log('Enhanced behavior tests passed');
