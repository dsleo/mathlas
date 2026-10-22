import { fixed } from './methodShared'

export type P = [number, number]
export type Anchor = 'start' | 'end' | 'middle'

/** 0 below `a`, 1 above `b`, a straight ramp between: how far a detail has faded in at zoom `k`. */
export const fade = (k: number, a: number, b: number) => Math.max(0, Math.min(1, (k - a) / (b - a)))

/** A small deterministic random-number generator, so every island is drawn the same on every load. */
export function seeded(key: string) {
  let h = 0
  for (let i = 0; i < key.length; i++) h = (h * 31 + key.charCodeAt(i)) >>> 0
  return () => { h = (h * 1664525 + 1013904223) >>> 0; return h / 4294967296 }
}

export function hull(points: P[]) {
  const p = [...points].sort((a, b) => a[0] - b[0] || a[1] - b[1])
  const cross = (o: number[], a: number[], b: number[]) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
  const lower: P[] = [], upper: P[] = []
  for (const q of p) { while (lower.length > 1 && cross(lower[lower.length - 2], lower[lower.length - 1], q) <= 0) lower.pop(); lower.push(q) }
  for (const q of [...p].reverse()) { while (upper.length > 1 && cross(upper[upper.length - 2], upper[upper.length - 1], q) <= 0) upper.pop(); upper.push(q) }
  lower.pop(); upper.pop()
  return lower.concat(upper)
}

export function smooth(points: P[]) {
  const mid = (a: P, b: P): P => [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]
  const start = mid(points[points.length - 1], points[0])
  let d = `M${fixed(start[0])},${fixed(start[1])}`
  points.forEach((p, i) => { const e = mid(p, points[(i + 1) % points.length]); d += `Q${fixed(p[0])},${fixed(p[1])} ${fixed(e[0])},${fixed(e[1])}` })
  return `${d}Z`
}

export const within = (p: P, poly: P[]) => {
  let hit = false
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const [xi, yi] = poly[i], [xj, yj] = poly[j]
    if ((yi > p[1]) !== (yj > p[1]) && p[0] < ((xj - xi) * (p[1] - yi)) / (yj - yi) + xi) hit = !hit
  }
  return hit
}
export const quad = (a: P, c: P, b: P, n = 14): P[] => Array.from({ length: n + 1 }, (_, i) => {
  const t = i / n
  return [(1 - t) * (1 - t) * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0], (1 - t) * (1 - t) * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1]] as P
})
export const polyline = (pts: P[]) => pts.map((p, i) => `${i ? 'L' : 'M'}${fixed(p[0])},${fixed(p[1])}`).join('')
export const disc = (x: number, y: number, r: number) => `M${fixed(x - r)},${fixed(y)}a${fixed(r)},${fixed(r)} 0 1,0 ${fixed(2 * r)},0a${fixed(r)},${fixed(r)} 0 1,0 ${fixed(-2 * r)},0Z`
export function waypoints(pts: P[], every = 72): P[] {
  const out: P[] = []
  let run = every / 2
  for (let i = 1; i < pts.length; i++) {
    run += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])
    if (run >= every) { out.push(pts[i]); run = 0 }
  }
  return out
}
