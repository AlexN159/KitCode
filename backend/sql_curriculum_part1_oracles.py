"""Static offline-generated expected outputs for SQL curriculum part one."""
from __future__ import annotations

import base64
import json
import zlib

# This is a compressed literal JSON snapshot generated during authoring.  It
# decodes data only; catalogue import never opens a database or evaluates SQL.
_PAYLOAD = (
    "c-rk;O>g5i5dAMcuLE&NN>&d6`n^5(Snt8e25o>q*>0Rg7e)Vj$)PAelA>X4WXXsHI50UBXWl%{$PzWmzpLlJAJ=y;pLhHFk84qg)pviazW=z}?&Y@m>HdDZ7u)97haG?aaNlhA#kTqJD}Vj`_`u)4JpIGp?{|;pd-cxESKl~)+x+(BE9jwD;_!aZD{;u|d{%$VKF<R`hS~q{E?Oh9Ys5ON0oK9|Hp4B}XstP2X2761I)iPUGWRt`4l~%?pt-|s_!+G=J2#<HcHu6}hl(y%_I1%}Rc1hRtLYD8m4b&(p2N5Y+QGxv=8!4JlrcMsk4jikmKEU$<(W2UP2V|C6dcUtXtv7iu<0`O8#gMqdk*KyjViYiOjp}y0CqANn3rLU=JAZzwbtHPXZ!3lUd|$=F{n?8LDRRVfLTH^vMt(moIYa3Me%Svo)L<i0LmGoJzf89x*Rzd%AvU+XN&<E<${{{?0rEzTuLs;DRV)Fxu8bQg{sX3DoCvhVLrx2!GBg&CpK1O!CI}sPHYY-tzt9QXfG$$qOIJ3YATTPT>EF_CCH@%OjiHK%O&gK^)$+w8sy4ngDxDOBj6VW3@C7*$1#!_$8^7AlKLG}MaD5*^f+drmi>;^8OL-6f04mYnT4q{3sdD5raIHY*xa`RDid*a#xap`Y?E=U%sEz$=h)DU>A}hP`*6z5d^m?@_F;h~Pv8@s%4LS?xy9PFr?Jk*8|O}&G@AR8@7AodlKYzP*mO5ua=+pvyK(Mm@70ZiUpdqp?$_LBP_+>_x{o4ozX#5wo)S{oX`rY-KPfQ+js}<IbRm#p1k+m_>a%69a+$QzF(e~MQ>YG82q97c5WyiZ3Sc3mz&eF=#C9M>*5XWd%gFA8?x7tB^feXJ*+o0&(|no-5T_!HQjx}}5d|??28on|QU&RggCdI1eBg5#Wo!_pXR=$)=O7vq;Td@{yQhTd2&zx>p)R6GjqE0YD%wDOe)zL_`4n7)Sx|}C-MA%U%{OqNn6JUC2Z@*%ekitAT8@?slus|8@BZ37--iP;f!W>dAHEn0F9OUcixhk029AK~p@1$eW~PHeYucpQMQwKV#IDT6kvax3R>b!$M?l8M+uIYzSQb*xKshs{VaqrHpwX7CC+p-?poWF}oGcB2l;oi7**L__0~u~7L~Rj{s<17>9SR+7|FBoMA%X2^REBL4Ze~!}7O<ruL9=v6hNCLln@D$CMx=v+(?-yK`(%lTxFtGfPZpUt{6^@wqV;!n&*pIQi=n#WprS1<@)bO$b8FjNfYkO)(-(+wpDT~}F&K4%Tif^bVy;SwAB73-+}gIU0<#areErV2=6&gs725WQcuoW0%HHe~!?~$AZr&4R1x(bmc%}&i5DpB6Bwx5>C%E&%8$!G$gv&s@_QM;Eu3bTU1MT|Iwp%`38|(_OE5NP*y8`SAuq(i>0J{S064)iMOJJA4E`ePFy99O#>=M`|uq(l??CcV7PQW<<=LDP+a8AHE0p|pq6L3zzIRWPcoD*<Pz&Qcu1e_CaPQW<<=LDP+a8AHE0p|pq6L3zzIRWPcoD*;^fm;dOO5nD=6Iz0P3Hs{|`sJ*@B*4`r0JJr<%Ox?E#JGyYz(8LDdI{(^eyJl33$QTD*?mcdt4xMu2Z&!(DeX4xUYb;Kbt-Mk$dqeQkIe1}r}`?`QQ~6`9Jm6X4vu@t@$ftJ4M)=%bw@|jYjpRNnYGo#4cX1}#w>ir+xHDWc{)X;qK;1cr4=QX+ak<FLECA+0*xwc#VUzw<{V6IiRoI2z_t#8US$Gaow5%Wcw4jbZxZ_fa__U`4@d<5NbO!`IUI1JZZ6h(zk5s(bFD}ofcYdS6A<2J)&JTv`Dfu=4Cd-d53gm|o@(FqalN*{%ylYPOV7Qweoc>}g+|d5c%(+r5@OL~C^-VfzIfoYB+JGRq_`N`7${twcH8w;+g@7qR7{iZ9%vE#cLjc!a1fZr?@y0Uu4O*%pBJn?{P#Z#1f)F"
)
ORACLE_OUTPUTS = {
    key: tuple(values)
    for key, values in json.loads(zlib.decompress(base64.b85decode(_PAYLOAD)).decode("utf-8")).items()
}

# The local SQL judge deliberately renders a database NULL as the visible
# token ``NULL``. These two window reports place NULL only in their final
# column; align the offline snapshot with that production output contract.
for _key in ("sql-curated-109", "sql-curated-110"):
    ORACLE_OUTPUTS[_key] = tuple(
        "\n".join(f"{line}NULL" if line.endswith("\t") else line for line in value.split("\n"))
        for value in ORACLE_OUTPUTS[_key]
    )
