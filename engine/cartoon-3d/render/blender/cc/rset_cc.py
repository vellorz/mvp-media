# render speed settings (r1 test: S09 f889 8 spp 89 s vs 4 spp + these bounces 53 s, mean abs diff 1.4/255, no visible change)
import bpy
sc=bpy.context.scene; sc.cycles.transparent_max_bounces=8; sc.cycles.diffuse_bounces=1; sc.cycles.max_bounces=3
