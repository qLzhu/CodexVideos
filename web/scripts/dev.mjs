import http from 'node:http';
import { createReadStream, existsSync } from 'node:fs';
import { extname, join, resolve } from 'node:path';

const root = resolve(process.cwd(), 'src');
const port = Number(process.env.PORT || 5173);
const mime = { '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css', '.json': 'application/json' };

http.createServer((req, res) => {
  const urlPath = req.url === '/' ? '/index.html' : req.url.split('?')[0];
  const filePath = join(root, urlPath);
  if (!existsSync(filePath)) {
    res.writeHead(404); res.end('Not found'); return;
  }
  res.writeHead(200, { 'Content-Type': mime[extname(filePath)] || 'text/plain' });
  createReadStream(filePath).pipe(res);
}).listen(port, () => console.log(`WebUI dev server at http://localhost:${port}`));
