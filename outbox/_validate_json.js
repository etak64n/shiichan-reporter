const fs = require('fs');
for (const path of process.argv.slice(2)) {
  try {
    JSON.parse(fs.readFileSync(path, 'utf8'));
    console.log(path, 'VALID');
  } catch (e) {
    console.log(path, 'INVALID:', e.message);
  }
}
