// Draws every field of the time-lapse with the same terrain generator as Proofscape's proof map (src/worldTerrain.ts),
// once, at the island's final size: contours, rivers, forests, mountains and the clearings under the event symbols.
// The page scales that drawing as the field grows. Output: public/data/field-film-art.json
import { build } from 'esbuild'
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { pathToFileURL } from 'node:url'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const stub = { name: 'stub', setup(b) {
  b.onResolve({ filter: /methodShared$/ }, () => ({ path: 'methodShared', namespace: 'stub' }))
  b.onLoad({ filter: /.*/, namespace: 'stub' }, () => ({ contents: 'export const fixed = (value) => value.toFixed(1)', loader: 'js' }))
} }
const entry = `export { terrain } from ${JSON.stringify(root + '/src/worldTerrain.ts')}\nexport { seeded, smooth } from ${JSON.stringify(root + '/src/worldShared.ts')}`
mkdirSync(root + '/.cache', { recursive: true })
const out = root + '/.cache/film-terrain.mjs'
await build({ stdin: { contents: entry, resolveDir: root, loader: 'ts' }, bundle: true, format: 'esm', platform: 'node', outfile: out, plugins: [stub], logLevel: 'error' })
const { terrain, seeded, smooth } = await import(pathToFileURL(out).href)

const film = JSON.parse(readFileSync(root + '/data/field-film.json', 'utf8'))
const [W, H] = film.box
const FAMILY = JSON.parse(readFileSync(root + '/data/field-film-families.json', 'utf8'))
const f1 = (v) => v.toFixed(1)
const radius = (n) => 4.6 * (3 + 2.3 * Math.sqrt(n))

const islands = film.fields.map((f) => {
  const R = radius(f.events), rnd = seeded(f.id + '-shape'), n = 13, base = []
  for (let k = 0; k < n; k++) {
    const a = (2 * Math.PI * k) / n, rr = 0.88 + 0.24 * rnd()
    base.push([f.x + rr * Math.cos(a) * 1.18 * R, f.y + rr * Math.sin(a) * 0.88 * R])
  }
  // sample the closed Catmull-Rom curve through the points into a polygon ring
  const ring = []
  for (let k = 0; k < n; k++) {
    const p0 = base[(k - 1 + n) % n], p1 = base[k], p2 = base[(k + 1) % n], p3 = base[(k + 2) % n]
    const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6], c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6]
    for (let j = 0; j < 8; j++) {
      const t = j / 8, m = 1 - t
      ring.push([m * m * m * p1[0] + 3 * m * m * t * c1[0] + 3 * m * t * t * c2[0] + t * t * t * p2[0], m * m * m * p1[1] + 3 * m * m * t * c1[1] + 3 * m * t * t * c2[1] + t * t * t * p2[1]])
    }
  }
  const sites = film.events.filter((e) => e.field === f.id).map((e) => [f.x + e.x * R * 0.98, f.y + e.z * R * 0.98])
  const land = terrain(FAMILY[f.id], ring, [f.x, f.y], sites, seeded(f.id + '-terrain'))
  // distance from the centre to the shore, by angle, so bridges can land on the coast at any size
  const polar = Array.from({ length: 72 }, (_, i) => {
    const a = (i / 72) * 2 * Math.PI, ux = Math.cos(a), uy = Math.sin(a)
    let best = 0
    for (let t = 0; t < 400; t += 2) {
      const x = f.x + ux * t, y = f.y + uy * t
      let hit = false
      for (let i2 = 0, j2 = ring.length - 1; i2 < ring.length; j2 = i2++) {
        const [xi, yi] = ring[i2], [xj, yj] = ring[j2]
        if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) hit = !hit
      }
      if (hit) best = t
    }
    return Math.round(best)
  })
  return {
    id: f.id, family: FAMILY[f.id], cx: f.x, cy: f.y, R, polar, top: Math.min(...ring.map((p) => p[1])) - f.y, bottom: Math.max(...ring.map((p) => p[1])) - f.y,
    path: smooth(ring), halo: smooth(land.ripples[1]), near: smooth(land.ripples[0]),
    minor: land.minor, major: land.major, lakes: land.lakes, rivers: land.rivers.map((r) => r.water), fields: land.fields, squares: land.squares, dunes: land.dunes, spirals: land.spirals,
    mountains: land.mountains, hatch: land.hatch, ink: land.ink, treeD: land.trees.map((t) => t.d).join(''), treeH: land.trees.map((t) => t.hatch).join(''),
  }
})

// the little dashes of the sea
const sea = seeded('film-sea')
let wisps = ''
for (let tries = 0, n = 0; tries < 4000 && n < 260; tries++) {
  const x = -80 + sea() * (W + 160), y = -80 + sea() * (H + 160)
  if (islands.some((i) => Math.hypot(i.cx - x, i.cy - y) < i.R * 1.45 + 36)) continue
  n++
  const w = 14 + sea() * 26
  wisps += `M${f1(x)},${f1(y)}q${f1(w / 2)},-5 ${f1(w)},0q${f1(-w / 2)},4 ${f1(-w)},0Z`
}
mkdirSync(root + '/public/data', { recursive: true })
writeFileSync(root + '/public/data/field-film-art.json', JSON.stringify({ islands, wisps }))
console.log(`drew ${islands.length} islands (${Math.round(JSON.stringify(islands).length / 1024)} KB)`)
