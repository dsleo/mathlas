type P = [number, number]

export type Terrain = {
  minor: string
  major: string
  rivers: { bank: string; water: string }[]
  mountains: string
  hatch: string
  trees: { y: number; d: string; hatch: string }[]
  ink: string
  fields: string
  squares: string
  dunes: string
  spirals: string
  lakes: string
  ripples: P[][]
  /** water-covered cells at rising sea levels, for the flood easter egg */
  flood: { level: number; d: string }[]
  /** height (0 coast, ~1 summit) under each input site, in the order given */
  siteH: number[]
}

const f = (n: number) => n.toFixed(1)

function inside(p: P, poly: P[]) {
  let hit = false
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const [xi, yi] = poly[i], [xj, yj] = poly[j]
    if ((yi > p[1]) !== (yj > p[1]) && p[0] < ((xj - xi) * (p[1] - yi)) / (yj - yi) + xi) hit = !hit
  }
  return hit
}

export function polygonArea(poly: P[]) {
  let a = 0
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) a += (poly[j][0] + poly[i][0]) * (poly[j][1] - poly[i][1])
  return Math.abs(a / 2)
}

const smoothstep = (t: number) => { const c = Math.max(0, Math.min(1, t)); return c * c * (3 - 2 * c) }

// ---- hand-drawn glyphs ---------------------------------------------------------------------------------------------
function peak(x: number, y: number, s: number, rnd: () => number) {
  const w = s * 1.15, h = s
  const jag = () => (rnd() - 0.5) * s * 0.12
  const pts: P[] = [[x - w, y], [x - w * 0.55, y - h * 0.5 + jag()], [x - w * 0.3, y - h * 0.42 + jag()], [x + w * 0.02, y - h], [x + w * 0.32, y - h * 0.52 + jag()], [x + w * 0.58, y - h * 0.64 + jag()], [x + w, y]]
  const outline = pts.map((p, i) => `${i ? 'L' : 'M'}${f(p[0])},${f(p[1])}`).join('')
  let hatch = ''
  for (let i = 3; i < pts.length - 1; i++) {
    const a = pts[i], b = pts[i + 1], steps = Math.max(2, Math.round(Math.hypot(b[0] - a[0], b[1] - a[1]) / 3.4))
    for (let k = 1; k < steps; k++) {
      const u = k / steps, sx = a[0] + (b[0] - a[0]) * u, sy = a[1] + (b[1] - a[1]) * u
      hatch += `M${f(sx)},${f(sy)}l${f(s * 0.17)},${f(Math.min(s * 0.5, (y - sy) * 0.8))}`
    }
  }
  return { outline: `${outline}`, hatch, base: `M${f(x - w * 1.05)},${f(y)}H${f(x + w * 1.05)}` }
}

type Tree = { d: string; hatch: string }
const TAU = Math.PI * 2
const pathOf = (pts: P[]) => `M${pts.map((p) => `${f(p[0])},${f(p[1])}`).join('L')}Z`

/** A fir: a stepped silhouette on a short trunk, shaded on its right. */
function conifer(x: number, y: number, s: number): Tree {
  const shape: P[] = [[-1, 0], [-1, -2], [-5.5, -2], [-2.6, -6.5], [-4.6, -6.5], [-2.2, -11], [-3.8, -11], [0, -17.5], [3.8, -11], [2.2, -11], [4.6, -6.5], [2.6, -6.5], [5.5, -2], [1, -2], [1, 0]]
  let hatch = ''
  for (const [yb, w] of [[-2, 4.4], [-6.5, 3.6], [-11, 2.6]]) hatch += `M${f(x + 1.3 * s)},${f(y + (yb - 3.4) * s)}L${f(x + w * s)},${f(y + yb * s)}M${f(x + 1.3 * s)},${f(y + (yb - 1.6) * s)}L${f(x + (w - 0.9) * s)},${f(y + yb * s)}`
  return { d: pathOf(shape.map(([a, b]) => [x + a * s, y + b * s] as P)), hatch }
}

/** A broadleaf tree: a scalloped crown on a trunk, with a crescent of shade. */
function broadleaf(x: number, y: number, s: number, rnd: () => number): Tree {
  const cx = x, cy = y - 9.5 * s, r = 6.4 * s, n = 7 + Math.floor(rnd() * 3), phase = rnd() * TAU
  const vertex = (i: number): P => [cx + Math.cos(phase + (i / n) * TAU) * r, cy + Math.sin(phase + (i / n) * TAU) * r * 0.9]
  const bulge = (i: number): P => [cx + Math.cos(phase + ((i + 0.5) / n) * TAU) * r * 1.38, cy + Math.sin(phase + ((i + 0.5) / n) * TAU) * r * 1.24]
  let d = `M${f(x)},${f(y)}V${f(y - 4.2 * s)}M${f(vertex(0)[0])},${f(vertex(0)[1])}`
  for (let i = 0; i < n; i++) { const c = bulge(i), v = vertex((i + 1) % n); d += `Q${f(c[0])},${f(c[1])} ${f(v[0])},${f(v[1])}` }
  return { d: `${d}Z`, hatch: `M${f(cx + 1.2 * s)},${f(cy + 5.6 * s)}Q${f(cx + 5.8 * s)},${f(cy + 4.4 * s)} ${f(cx + 7.4 * s)},${f(cy - 0.6 * s)}M${f(cx - 2.5 * s)},${f(cy - 1 * s)}q${f(1.2 * s)},${f(-2.6 * s)} ${f(3 * s)},${f(-3 * s)}` }
}

/** A palm: a leaning trunk under a rosette of leaf blades. */
function palm(x: number, y: number, s: number, rnd: () => number): Tree {
  const lean = (rnd() - 0.5) * 7 * s, tx = x + lean, ty = y - 15 * s
  let d = `M${f(x)},${f(y)}Q${f(x + lean * 1.6)},${f(y - 8 * s)} ${f(tx)},${f(ty)}`
  for (const a of [-2.9, -2.3, -1.75, -1.15, -0.55, -0.1]) {
    const ex = tx + Math.cos(a) * 9.5 * s, ey = ty + Math.sin(a) * 6 * s + 3.4 * s
    const mx = (tx + ex) / 2, my = (ty + ey) / 2 - 4.2 * s
    d += `M${f(tx)},${f(ty)}Q${f(mx - 1.6 * s)},${f(my - 1 * s)} ${f(ex)},${f(ey)}Q${f(mx + 1.6 * s)},${f(my + 2 * s)} ${f(tx)},${f(ty)}Z`
  }
  return { d, hatch: `M${f(x + lean * 0.5 + 0.9 * s)},${f(y - 4 * s)}l${f(0.6 * s)},${f(-4 * s)}` }
}

// ---- one landmark family per domain, drawn in the same thin ink ------------------------------------------------------
const mill = (x: number, y: number, s: number) => `M${f(x - 5 * s)},${f(y)}L${f(x - 3.4 * s)},${f(y - 11 * s)}H${f(x + 3.4 * s)}L${f(x + 5 * s)},${f(y)}ZM${f(x)},${f(y - 11 * s)}L${f(x - 11 * s)},${f(y - 19 * s)}M${f(x)},${f(y - 11 * s)}L${f(x + 11 * s)},${f(y - 19 * s)}M${f(x)},${f(y - 11 * s)}L${f(x - 9 * s)},${f(y - 2 * s)}M${f(x)},${f(y - 11 * s)}L${f(x + 9 * s)},${f(y - 3 * s)}`
const crystals = (x: number, y: number, s: number) => [[0, 0, 1], [-9, 4, 0.7], [8, 3, 0.8]].map(([dx, dy, k]) => `M${f(x + dx * s)},${f(y + dy * s)}l${f(-4 * k * s)},${f(-6 * k * s)}l${f(4 * k * s)},${f(-12 * k * s)}l${f(4 * k * s)},${f(12 * k * s)}l${f(-4 * k * s)},${f(6 * k * s)}ZM${f(x + dx * s)},${f(y + dy * s)}V${f(y + (dy - 18) * s * k)}`).join('')
const obelisk = (x: number, y: number, s: number) => `M${f(x - 3 * s)},${f(y)}L${f(x - 2 * s)},${f(y - 20 * s)}L${f(x)},${f(y - 25 * s)}L${f(x + 2 * s)},${f(y - 20 * s)}L${f(x + 3 * s)},${f(y)}ZM${f(x - 6 * s)},${f(y)}H${f(x + 6 * s)}M${f(x)},${f(y - 25 * s)}V${f(y)}`
const terraces = (x: number, y: number, s: number) => [0, 1, 2, 3].map((i) => `M${f(x - (24 - i * 5) * s)},${f(y - i * 5 * s)}Q${f(x)},${f(y - (14 + i * 5) * s)} ${f(x + (24 - i * 5) * s)},${f(y - i * 5 * s)}`).join('')
const lighthouse = (x: number, y: number, s: number) => `M${f(x - 6 * s)},${f(y)}L${f(x - 3.5 * s)},${f(y - 24 * s)}H${f(x + 3.5 * s)}L${f(x + 6 * s)},${f(y)}ZM${f(x - 5 * s)},${f(y - 24 * s)}H${f(x + 5 * s)}M${f(x - 3 * s)},${f(y - 24 * s)}L${f(x)},${f(y - 31 * s)}L${f(x + 3 * s)},${f(y - 24 * s)}M${f(x + 5 * s)},${f(y - 26 * s)}L${f(x + 22 * s)},${f(y - 32 * s)}M${f(x + 5 * s)},${f(y - 26 * s)}L${f(x + 22 * s)},${f(y - 20 * s)}`
const ziggurat = (x: number, y: number, s: number) => [0, 1, 2].map((i) => `M${f(x - (18 - i * 5) * s)},${f(y - i * 7 * s)}H${f(x + (18 - i * 5) * s)}V${f(y - (i + 1) * 7 * s)}H${f(x - (18 - i * 5) * s)}Z`).join('')
const pillars = (x: number, y: number, s: number) => `M${f(x - 14 * s)},${f(y)}V${f(y - 20 * s)}M${f(x)},${f(y)}V${f(y - 24 * s)}M${f(x + 14 * s)},${f(y)}V${f(y - 18 * s)}M${f(x - 18 * s)},${f(y - 20 * s)}H${f(x + 4 * s)}M${f(x - 4 * s)},${f(y - 24 * s)}H${f(x + 18 * s)}`
const archway = (x: number, y: number, s: number) => `M${f(x - 10 * s)},${f(y)}V${f(y - 14 * s)}a${10 * s},${10 * s} 0 0,1 ${20 * s},0V${f(y)}M${f(x - 15 * s)},${f(y)}H${f(x + 15 * s)}`
type Glyph = (x: number, y: number, s: number) => string
// what stands on each island besides the terrain itself; [glyphs, how many]
const landmark: Record<string, [Glyph[], number]> = {
  analytic: [[mill], 2], algebraic: [[crystals], 6], geometric: [[obelisk, ziggurat], 4], discrete: [[mill, archway], 3], logic: [[lighthouse, pillars, terraces], 4],
}
// the character of each island: jungle, crystal badlands, formal terraces, farmland, spiral hills, dunes
const biome: Record<string, { peaks: number; trees: number; leafy: number; rivers: number; lake: boolean; fields: number; squares: number; dunes: number; spirals: number }> = {
  analytic: { peaks: 0.8, trees: 3.4, leafy: 0.95, rivers: 3, lake: true, fields: 0, squares: 0, dunes: 0, spirals: 0 },
  algebraic: { peaks: 1.8, trees: 0.3, leafy: 0.1, rivers: 1, lake: false, fields: 0, squares: 0, dunes: 0, spirals: 0 },
  geometric: { peaks: 0.9, trees: 0.7, leafy: 0.4, rivers: 1, lake: false, fields: 0, squares: 4, dunes: 0, spirals: 0 },
  discrete: { peaks: 0.4, trees: 1.1, leafy: 0.9, rivers: 1, lake: true, fields: 7, squares: 0, dunes: 0, spirals: 0 },
  logic: { peaks: 0.7, trees: 0.2, leafy: 0, rivers: 0, lake: false, fields: 0, squares: 0, dunes: 9, spirals: 4 },
}

/** A heightfield-driven pen-and-ink landscape for one island. */
export function terrain(family: string, ring: P[], centre: P, sites: P[], rnd: () => number): Terrain {
  const g = 7
  const xs = ring.map((p) => p[0]), ys = ring.map((p) => p[1])
  const x0 = Math.floor(Math.min(...xs) - 8), y0 = Math.floor(Math.min(...ys) - 8)
  const nx = Math.ceil((Math.max(...xs) - x0 + 16) / g) + 1, ny = Math.ceil((Math.max(...ys) - y0 + 16) / g) + 1
  const node = (i: number, j: number): P => [x0 + i * g, y0 + j * g]
  const ins = new Uint8Array(nx * ny), dist = new Float32Array(nx * ny)
  let maxD = 1
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
    const p = node(i, j)
    if (!inside(p, ring)) continue
    ins[j * nx + i] = 1
    let d = 1e9
    for (const q of ring) d = Math.min(d, Math.hypot(q[0] - p[0], q[1] - p[1]))
    dist[j * nx + i] = d
    if (d > maxD) maxD = d
  }
  const table = Array.from({ length: 36 * 36 }, () => rnd())
  const vn = (x: number, y: number) => {
    const gx = Math.floor(x), gy = Math.floor(y), tx = smoothstep(x - gx), ty = smoothstep(y - gy)
    const at = (a: number, b: number) => table[(((b % 36) + 36) % 36) * 36 + (((a % 36) + 36) % 36)]
    return (at(gx, gy) * (1 - tx) + at(gx + 1, gy) * tx) * (1 - ty) + (at(gx, gy + 1) * (1 - tx) + at(gx + 1, gy + 1) * tx) * ty
  }
  const bio = biome[family] ?? biome.analytic
  const crest = Math.max(1, Math.round((polygonArea(ring) / 26000) * bio.peaks))
  // a drawn thing of half-width w and height h at (x, y) must lie wholly on land
  // a point is on land, clear of the coast, if its grid cell is inside and far enough from the ring
  const onLand = (a: number, b: number) => {
    const i = Math.round((a - x0) / g), j = Math.round((b - y0) / g)
    if (i < 0 || j < 0 || i >= nx || j >= ny) return false
    const k = j * nx + i
    return ins[k] === 1 && dist[k] > 9
  }
  const fits = (x: number, y: number, w: number, h: number) => [[x - w, y], [x + w, y], [x, y - h], [x - w, y - h * 0.5], [x + w, y - h * 0.5], [x, y + 3]].every(([a, b]) => onLand(a, b))
  const peaks: { p: P; a: number; s: number }[] = []
  const cands: P[] = []
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) if (ins[j * nx + i] && dist[j * nx + i] > maxD * 0.42) cands.push(node(i, j))
  for (let k = 0; k < crest && cands.length; k++) {
    for (let t = 0; t < 60; t++) {
      const p = cands[Math.floor(rnd() * cands.length)]
      if (peaks.every((q) => Math.hypot(q.p[0] - p[0], q.p[1] - p[1]) > 80)) { peaks.push({ p, a: 0.55 + rnd() * 0.45, s: 34 + rnd() * 26 }); break }
    }
  }
  if (!peaks.length) peaks.push({ p: centre, a: 0.8, s: 50 })
  const hv = new Float32Array(nx * ny)
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
    const k = j * nx + i
    if (!ins[k]) continue
    const [x, y] = node(i, j)
    let h = 0.46 * smoothstep(dist[k] / (maxD * 0.85))
    for (const q of peaks) h += q.a * 0.62 * Math.exp(-((x - q.p[0]) ** 2 + (y - q.p[1]) ** 2) / (2 * q.s * q.s))
    h += 0.16 * (vn(x / 34, y / 34) - 0.5) + 0.07 * (vn(x / 13, y / 13) - 0.5)
    hv[k] = Math.max(0.001, Math.min(1, h))
  }
  // the sea at rising levels: row runs of the cells it would cover
  const flood: { level: number; d: string }[] = []
  for (const level of [0.08, 0.15, 0.22, 0.29, 0.36, 0.43, 0.5, 0.58, 0.66, 0.75, 0.85, 0.96]) {
    let d = ''
    for (let j = 0; j < ny; j++) {
      let run = -1
      for (let i = 0; i <= nx; i++) {
        const wet = i < nx && ins[j * nx + i] === 1 && hv[j * nx + i] <= level
        if (wet && run < 0) run = i
        if (!wet && run >= 0) {
          d += `M${f(x0 + run * g - g / 2)},${f(y0 + j * g - g / 2)}h${f((i - run) * g)}v${g}h${f(-(i - run) * g)}Z`
          run = -1
        }
      }
    }
    flood.push({ level, d })
  }
  const siteH = sites.map(([sx, sy]) => {
    const i = Math.round((sx - x0) / g), j = Math.round((sy - y0) / g)
    return i < 0 || j < 0 || i >= nx || j >= ny ? 0 : hv[j * nx + i]
  })
  // contour lines by marching squares
  const minor: string[] = [], major: string[] = []
  const levels = Array.from({ length: 13 }, (_, i) => 0.06 + i * 0.07)
  levels.forEach((L, li) => {
    const out: string[] = []
    for (let j = 0; j < ny - 1; j++) for (let i = 0; i < nx - 1; i++) {
      const tl = hv[j * nx + i], tr = hv[j * nx + i + 1], br = hv[(j + 1) * nx + i + 1], bl = hv[(j + 1) * nx + i]
      const c = (tl > L ? 8 : 0) + (tr > L ? 4 : 0) + (br > L ? 2 : 0) + (bl > L ? 1 : 0)
      if (c === 0 || c === 15) continue
      const [px, py] = node(i, j)
      const top = (): P => [px + ((L - tl) / (tr - tl)) * g, py]
      const right = (): P => [px + g, py + ((L - tr) / (br - tr)) * g]
      const bottom = (): P => [px + ((L - bl) / (br - bl)) * g, py + g]
      const left = (): P => [px, py + ((L - tl) / (bl - tl)) * g]
      const seg = (a: P, b: P) => out.push(`M${f(a[0])},${f(a[1])}L${f(b[0])},${f(b[1])}`)
      switch (c) {
        case 1: case 14: seg(left(), bottom()); break
        case 2: case 13: seg(bottom(), right()); break
        case 3: case 12: seg(left(), right()); break
        case 4: case 11: seg(top(), right()); break
        case 5: seg(top(), right()); seg(left(), bottom()); break
        case 6: case 9: seg(top(), bottom()); break
        case 7: case 8: seg(top(), left()); break
        case 10: seg(top(), left()); seg(bottom(), right()); break
      }
    }
    ;(li % 3 === 2 ? major : minor).push(out.join(''))
  })
  // rivers: steepest descent from the highest crests
  const rivers: { bank: string; water: string }[] = []
  const ranked = [...peaks].sort((a, b) => b.a - a.a)
  const sources = Array.from({ length: bio.rivers }, (_, n) => ({ p: [ranked[n % ranked.length].p[0] + (n >= ranked.length ? (rnd() - 0.5) * 70 : 0), ranked[n % ranked.length].p[1] + (n >= ranked.length ? (rnd() - 0.5) * 50 : 0)] as P }))
  for (const src of sources) {
    let i = Math.round((src.p[0] - x0) / g), j = Math.round((src.p[1] - y0) / g)
    if (i < 0 || j < 0 || i >= nx || j >= ny || !ins[j * nx + i]) continue
    const pts: P[] = [node(i, j)]
    for (let step = 0; step < 220; step++) {
      let best = hv[j * nx + i], bi = i, bj = j
      for (let dj = -1; dj <= 1; dj++) for (let di = -1; di <= 1; di++) {
        if (!di && !dj) continue
        const ni = i + di, nj = j + dj
        if (ni < 0 || nj < 0 || ni >= nx || nj >= ny) continue
        if (!ins[nj * nx + ni]) continue
        const v = hv[nj * nx + ni] + (rnd() - 0.5) * 0.012
        if (v < best) { best = v; bi = ni; bj = nj }
      }
      if (bi === i && bj === j) break
      i = bi; j = bj
      pts.push(node(i, j))
    }
    if (pts.length < 6) continue
    const line = (off: number) => pts.map((p, n) => {
      const a = pts[Math.max(0, n - 1)], b = pts[Math.min(pts.length - 1, n + 1)]
      const dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1
      return [p[0] - (dy / l) * off, p[1] + (dx / l) * off] as P
    })
    const path = (pp: P[]) => {
      let d = `M${f(pp[0][0])},${f(pp[0][1])}`
      for (let n = 1; n < pp.length - 1; n++) { const e: P = [(pp[n][0] + pp[n + 1][0]) / 2, (pp[n][1] + pp[n + 1][1]) / 2]; d += `Q${f(pp[n][0])},${f(pp[n][1])} ${f(e[0])},${f(e[1])}` }
      return d
    }
    rivers.push({ bank: `${path(line(1.7))}${path(line(-1.7))}`, water: path(line(0)) })
  }
  // mountains: only where the whole glyph stands on land
  let outline = '', hatch = ''
  for (const q of peaks) {
    const group: [number, number, number][] = [[q.p[0], q.p[1] + 12, 26 + q.a * 20], [q.p[0] - 34, q.p[1] + 22, 16 + q.a * 9], [q.p[0] + 36, q.p[1] + 24, 14 + q.a * 8]]
    for (const [x, y, sz] of group) {
      if (!fits(x, y, sz * 1.2, sz)) continue
      const m = peak(x, y, sz, rnd)
      outline += m.outline + m.base
      hatch += m.hatch
    }
  }
  const taken: P[] = [...sites, ...peaks.map((q) => q.p)]
  const free = (p: P, gap: number) => taken.every((q) => Math.hypot(q[0] - p[0], q[1] - p[1]) >= gap)
  const cell = (p: P) => Math.round((p[1] - y0) / g) * nx + Math.round((p[0] - x0) / g)
  const pick = (n: number, tries: number, ok: (_p: P, k: number) => boolean, gap: number, use: (p: P) => void) => {
    for (let c = 0, t = 0; c < n && t < tries; t++) {
      const p = node(Math.floor(rnd() * nx), Math.floor(rnd() * ny))
      const k = cell(p)
      if (!ins[k] || !ok(p, k) || !free(p, gap)) continue
      taken.push(p)
      c++
      use(p)
    }
  }
  // forests: how many and what kind is the island's character
  const trees: { y: number; d: string; hatch: string }[] = []
  pick(Math.round((polygonArea(ring) / 2300) * bio.trees), 1200, (_p, k) => dist[k] > 18 && hv[k] > 0.1 && hv[k] < 0.66, 34, (p) => {
    const n = 4 + Math.floor(rnd() * 5)
    for (let t = 0; t < n; t++) {
      const x = p[0] + (rnd() - 0.5) * 42, y = p[1] + (rnd() - 0.5) * 28, sc = 0.95 + rnd() * 0.5
      if (!fits(x, y, 7 * sc, 17 * sc)) continue
      const kind = rnd() < bio.leafy ? (family === 'analytic' && rnd() < 0.3 ? palm(x, y, sc, rnd) : broadleaf(x, y, sc, rnd)) : conifer(x, y, sc)
      trees.push({ y, ...kind })
    }
  })
  trees.sort((a, b) => a.y - b.y)
  // landmarks
  let ink = ''
  const [glyphs, want] = landmark[family] ?? landmark.analytic
  pick(want, 800, (_p, k) => dist[k] > 26 && hv[k] < 0.72, 54, (p) => {
    const sc = 1.3 + rnd() * 0.35
    if (!fits(p[0], p[1], 20 * sc, 30 * sc)) { taken.pop(); return }
    ink += glyphs[Math.floor(rnd() * glyphs.length)](p[0], p[1], sc)
  })
  // farmland: furrowed plots
  let fieldsPath = ''
  pick(bio.fields, 900, (_p, k) => dist[k] > 22 && hv[k] < 0.5, 46, (p) => {
    const w = 15 + rnd() * 9, h = 10 + rnd() * 6, a = (rnd() - 0.5) * 0.5, ca = Math.cos(a), sa = Math.sin(a)
    const at = (u: number, v: number): P => [p[0] + u * ca - v * sa, p[1] + u * sa + v * ca]
    const corners = [at(-w, -h), at(w, -h), at(w, h), at(-w, h)]
    if (!corners.every((c) => inside(c, ring) && dist[cell(c)] > 8)) return
    fieldsPath += `M${corners.map((c) => `${f(c[0])},${f(c[1])}`).join('L')}Z`
    for (let u = -w + 4.5; u < w - 1; u += 4.5) { const [x1, y1] = at(u, -h), [x2, y2] = at(u, h); fieldsPath += `M${f(x1)},${f(y1)}L${f(x2)},${f(y2)}` }
  })
  // formal plots: nested squares
  let squares = ''
  pick(bio.squares, 900, (_p, k) => dist[k] > 30 && hv[k] < 0.6, 56, (p) => {
    if (!fits(p[0], p[1] + 24, 28, 48)) return
    const a = rnd() * 0.3
    for (const r of [26, 18, 10]) {
      const c = Array.from({ length: 4 }, (_, n) => [p[0] + r * Math.cos(a + Math.PI / 4 + (n * Math.PI) / 2) * 1.2, p[1] + r * Math.sin(a + Math.PI / 4 + (n * Math.PI) / 2) * 0.9] as P)
      squares += `M${c.map((q) => `${f(q[0])},${f(q[1])}`).join('L')}Z`
    }
    squares += `M${f(p[0] - 30)},${f(p[1])}H${f(p[0] + 30)}M${f(p[0])},${f(p[1] - 22)}V${f(p[1] + 22)}`
  })
  // dunes
  let dunes = ''
  pick(bio.dunes, 1200, (_p, k) => dist[k] > 12, 26, (p) => {
    const w = 11 + rnd() * 7
    if (!fits(p[0], p[1] + 6, w * 2, 8)) return
    dunes += `M${f(p[0] - w)},${f(p[1])}q${f(w / 2)},${f(-7)} ${f(w)},0q${f(w / 2)},7 ${f(w)},0M${f(p[0] - w * 0.6)},${f(p[1] + 7)}q${f(w * 0.4)},${f(-5)} ${f(w * 0.8)},0`
  })
  // spiral hills
  let spirals = ''
  pick(bio.spirals, 900, (_p, k) => dist[k] > 30 && hv[k] < 0.7, 70, (p) => {
    const R = 24
    if (!fits(p[0], p[1] + R * 0.5, R * 1.1, R * 1.4)) return
    let d = ''
    for (let t = 0; t <= 3.4 * Math.PI * 2; t += 0.3) {
      const r = 1.5 + (R * t) / (3.4 * Math.PI * 2)
      d += `${d ? 'L' : 'M'}${f(p[0] + r * Math.cos(t))},${f(p[1] + r * Math.sin(t) * 0.7)}`
    }
    spirals += d
  })
  // lakes
  let lakes = ''
  if (bio.lake) {
    const low = cands.filter((c) => { const k = cell(c); return dist[k] > maxD * 0.5 && free(c, 60) })
    const p = low[Math.floor(rnd() * low.length)]
    if (p) {
      const rx = 15 + rnd() * 9, ry = rx * 0.6
      const pts = Array.from({ length: 9 }, (_, n) => [p[0] + Math.cos((n / 9) * Math.PI * 2) * rx * (0.8 + rnd() * 0.4), p[1] + Math.sin((n / 9) * Math.PI * 2) * ry * (0.8 + rnd() * 0.4)] as P)
      if (pts.every((q) => inside(q, ring))) {
        const mid = (a: P, b: P): P => [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]
        const st = mid(pts[8], pts[0])
        lakes = `M${f(st[0])},${f(st[1])}` + pts.map((q, n) => { const e = mid(q, pts[(n + 1) % 9]); return `Q${f(q[0])},${f(q[1])} ${f(e[0])},${f(e[1])}` }).join('') + 'Z'
      }
    }
  }
  const r0 = Math.sqrt(polygonArea(ring) / Math.PI)
  const ripples = [1 + 9 / r0, 1 + 20 / r0].map((k) => ring.map(([x, y]): P => [centre[0] + (x - centre[0]) * k, centre[1] + (y - centre[1]) * k]))
  return { minor: minor.join(''), major: major.join(''), rivers, mountains: outline, hatch, trees, ink, fields: fieldsPath, squares, dunes, spirals, lakes, ripples, flood, siteH }
}
