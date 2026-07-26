const fs = require('fs');
const path = 'outbox/aws-what-s-new-kiro-opus-sonnet-monitoring-launch-aws-govcloud-us.json';
const data = fs.readFileSync(path, 'utf8');
try {
  JSON.parse(data);
  console.log('OK parses fine');
} catch (e) {
  console.log('ERROR:', e.message);
}
const lines = data.split('\n');
console.log('num lines', lines.length);
const line6 = lines[5];
console.log('line6 length', line6.length);
const region = line6.slice(2060, 2140);
console.log('region:', JSON.stringify(region));
for (let i = 0; i < line6.length; i++) {
  const c = line6.charCodeAt(i);
  if (c <= 0x1f) {
    console.log('control char at index', i, 'code', c, 'context:', JSON.stringify(line6.slice(Math.max(0,i-30), i+10)));
  }
}
