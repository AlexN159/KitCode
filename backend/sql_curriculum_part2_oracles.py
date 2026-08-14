"""Static expected SQL outputs for curriculum part two."""
from __future__ import annotations

import base64
import json
import zlib

_PAYLOAD = (
    "c%1E7S#KOS4E`&IpR)^{bNDTG+@wI!mp)c~*xG}}$XeriCuxnM|GlEFkw)4>d)Q9Wg#piy6#0>&B#QIT`RdQ*?B?_1V(4yXm{jK%zn)*qKg56$5^{X{WwGp5VrbC$8_UO8YF;+4i*M%FTlh-<Z*L~}Ymfi^-9ij47XzBR!Izyh8WfFAepck_X`95`TcsBhC4%Q8mJf?10JhdF@p^d&D1pd5@m<#`Tz>fHhll=g5W^4s-%5d&^<mrM0^uoWPy6x9lbIt$tof_JUJ_e0uO`1J0P93va5kPfp;Bd5Mo)ahH^%4d^7`vSyKkBWWIct>vt)~F{1z9WN}MHA-<&HxL@a|Y^@60{(wqm_O+gB3+=^Z`%yDOVb)b$ADZed{6emq_vX{c?5s;TcP(FRRrAyL<+rq*nh_D&LYE-49gf#C&3|zg=bWvqUREcm79zYqi&oD<~3O5HSf(kW3zR->4A#}4kv0jy8*0Zv45X{J|Ni3-%aT;ifwg<XubX64VBG?=y`wpE3ysqaAx0JJnHZ^LirdT&jK)nT&o&rWQplUKF;g1&EhiPfI*w+)o1NWWz7BHo=gJE_sgLN}lB{Pi9P<vsI2+U(1b3C;maTW6_$5Sg4*C3MN!LG5l!6xSM(BL{S>{MW$-TP-Z_<FoBb58?aJ%UNHn&_;~;L|5kM6o3Xjt!$Tj4lw*Q4|ysYsQIYPcgz|%3?f6(NX;$bUA3iK@Y~ESe)l5-*)i67tqNjLG327lNZPs+W{6b;n}JcV6vlY-5skDJ-S*AR>*LtCTFOLB{hY#iqh-`z-m2iu%O6dZGqM#g_ubpX*M7Ck3<CbC?rc2@F)kd`it!=3Uid21W*-&CZdgB8YG^AsagV~G1e3wMe9%qUKDcsMG(A#Ae2BLW5A%U|CU?}AgJVb44R12zz}QFMWR20P~Ae1+_VH_rLX+TvxKlt5Su;)_;=Y!MKBy8YtxI6jczTB8tljfPHoq0tSu(!&|E!b=uEdc6vID6fHNa3Bf-%GI0okB;l!o3-{Q>a;@U<8_||n0u-?OCV|y!j1TpYYFFjbVkgaP#1||xi;}Yomg@o)0{qX4Iqn?FMib9fPP8($o4y@spkM<A>EUF@Ew5h6MZx#AY_1MnycJ&8CZ=^wiOBFhvk#S<G$Y8lw0I|%e10$!7|3kbYr<$u4?cf#$U4@~WCL%+&e$q)U>#=+?FAOZmCVGlx5{<f_b=miyR;D*5-!JZ=X^a8lhyEVI1I}(1sZd^ouo5lnl;9F2Boj6gIQet`rCZwL*p9yX*sWqEKP~PbVrvD%!eE@j+G({X!;)yad*EBSaH+1d+?~bJp2huIZg|$i`);G7*94WhS_JosG55{C^ftkGa-$6@H|UX6(Pf7ORUzE)C<!V$IvcO(ShtodI=xmMM?2AtY)ZrO_xZt{#y1BpsDHV3*NH->l+~v-o+e5)xpv~o9YMcON%7U7%}UTfA}u^v9efKipD+BU3lkOp)xzY2|Au3P#}6N|^ge?(TP8))6H{e_$ssrsCzFutTf(J~S3<snEi-x=2|`{cTuV+=y7G~@?R(v`xnvPtEJUoSO0Ek5RWQizuPA%v?_%iX@+nL!A#cR6>TY^@8(vkFfi()2%E)7Q-QB36U*1N`?<f#<R3PAWDw~6aPY7%Hc=s5NR|n0%{{hvQi*W"
)

ORACLE_OUTPUTS = {key: tuple(values) for key, values in json.loads(zlib.decompress(base64.b85decode(_PAYLOAD)).decode("utf-8")).items()}

# Each time-series report has no prior value in its first row. Keep this
# static snapshot aligned with the judge's explicit SQL NULL rendering.
for _key in ("sql-curated-129", "sql-curated-130"):
    ORACLE_OUTPUTS[_key] = tuple(
        "\n".join(f"{line}NULL" if line.endswith("\t") else line for line in value.split("\n"))
        for value in ORACLE_OUTPUTS[_key]
    )
