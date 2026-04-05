import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
import matplotlib
import platform
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Notoフォントを検索して指定
font_path = fm.findfont("Noto Sans CJK JP")
plt.rcParams['font.family'] = fm.FontProperties(fname=font_path).get_name()
st.set_page_config(
    page_title="農業統計研修 | 分布と仮説検定",
    page_icon="🥔",
    layout="wide"
)

# ── スタイル ──────────────────────────────────────────
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f4e8;
        border-radius: 6px 6px 0 0;
        padding: 8px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4a7c3f !important;
        color: white !important;
    }
    .concept-box {
        background: #f8fdf4;
        border-left: 4px solid #4a7c3f;
        padding: 14px 18px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .warning-box {
        background: #fff8e1;
        border-left: 4px solid #f9a825;
        padding: 14px 18px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .term-box {
        background: #e8f4fd;
        border-left: 4px solid #1565c0;
        padding: 14px 18px;
        border-radius: 4px;
        margin: 8px 0;
    }
    h2 { color: #2e4a1e; }
    h3 { color: #3d6b30; }
</style>
""", unsafe_allow_html=True)

# ── ヘッダー ──────────────────────────────────────────
st.title("🥔 農業統計研修　第1章：データの分布と仮説検定")
st.caption("ジャガイモ試験を例にした統計入門")
st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 正規分布（収量）",
    "🌱 二項分布（発芽）",
    "🦠 ポアソン分布（塊茎腐敗）",
    "📐 仮説検定の用語"
])

# ═══════════════════════════════════════════════════════════════
# TAB 1: 正規分布
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.subheader("正規分布 — 10a あたり収量（kg）を例に")

    st.markdown("""
    <div class="concept-box">
    <b>正規分布とは？</b><br>
    平均を中心に左右対称の釣り鐘型。<br>
    連続データで「取りうる値に理論上の上下限がない」ことが前提。
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### パラメータ設定")
        mean_val = st.slider("平均収量（kg/10a）", 0, 100, 40, step=1,
                             help="スライダーを0や100付近に動かして分布の変化を観察")
        sd_val = st.slider("標準偏差（kg/10a）", 1, 30, 10, step=1)

        # 警告判定
        prob_negative = stats.norm.cdf(0, loc=mean_val, scale=sd_val)
        prob_over100  = 1 - stats.norm.cdf(100, loc=mean_val, scale=sd_val)

        st.metric("0 kg 以下になる確率", f"{prob_negative*100:.1f}%",
                  delta="⚠️ 物理的に不可能" if prob_negative > 0.01 else "問題なし",
                  delta_color="inverse")
        st.metric("100 kg 超になる確率", f"{prob_over100*100:.1f}%",
                  delta="⚠️ 上限超え" if prob_over100 > 0.01 else "問題なし",
                  delta_color="inverse")

    with col2:
        x = np.linspace(-30, 140, 500)
        y = stats.norm.pdf(x, loc=mean_val, scale=sd_val)

        fig, ax = plt.subplots(figsize=(7, 4))

        # 実用範囲外を赤でハイライト
        ax.fill_between(x, y, where=(x < 0), color='#e53935', alpha=0.5,
                        label='0 kg 以下（物理的に不可能）')
        ax.fill_between(x, y, where=(x > 100), color='#ff9800', alpha=0.5,
                        label='100 kg 超（現実的上限超え）')
        ax.fill_between(x, y, where=((x >= 0) & (x <= 100)), color='#66bb6a', alpha=0.4,
                        label='実用範囲（0〜100 kg）')
        ax.plot(x, y, color='#2e7d32', linewidth=2)

        ax.axvline(0,   color='#e53935', linestyle='--', alpha=0.7)
        ax.axvline(100, color='#ff9800', linestyle='--', alpha=0.7)
        ax.axvline(mean_val, color='#1b5e20', linestyle='-', linewidth=1.5)

        ax.set_xlabel("収量（kg/10a）", fontsize=11)
        ax.set_ylabel("確率密度", fontsize=11)
        ax.set_title(f"正規分布  μ={mean_val}, σ={sd_val}", fontsize=12)
        ax.legend(fontsize=9, loc='upper right')
        ax.set_xlim(-30, 140)
        ax.set_ylim(bottom=0)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.markdown("""
    <div class="warning-box">
    <b>⚠️ 正規分布の限界</b><br>
    正規分布は理論上 −∞〜+∞ の値をとる。<br>
    収量のように 0〜100 の範囲に収まるデータに正規分布を仮定すると、
    平均が端に近いほど「負の収量」や「100kg超」を想定してしまう。<br>
    → 割合データには <b>二項分布</b> や <b>ベータ分布</b> を検討する。
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# TAB 2: 二項分布
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.subheader("二項分布 — 発芽の有無を例に")

    st.markdown("""
    <div class="concept-box">
    <b>二項分布とは？</b><br>
    「成功か失敗か」の 2 値結果を n 回繰り返したときの成功数の分布。<br>
    パラメータ：試行数 n、成功確率 p
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### パラメータ設定")
        n_seeds = st.slider("播種数（粒）", 10, 200, 50, step=10)
        p_germ  = st.slider("発芽率（推定）", 0.0, 1.0, 0.80, step=0.05,
                             format="%.2f")

        expected = n_seeds * p_germ
        sd_binom  = np.sqrt(n_seeds * p_germ * (1 - p_germ))
        st.metric("期待発芽数", f"{expected:.1f} 粒")
        st.metric("標準偏差",   f"{sd_binom:.1f} 粒")
        st.metric("発芽率 95% 信頼区間（概算）",
                  f"{max(0,(expected-1.96*sd_binom)/n_seeds*100):.1f}〜"
                  f"{min(100,(expected+1.96*sd_binom)/n_seeds*100):.1f}%")

    with col2:
        k = np.arange(0, n_seeds + 1)
        pmf = stats.binom.pmf(k, n=n_seeds, p=p_germ)

        fig, ax = plt.subplots(figsize=(7, 4))
        colors = ['#388e3c' if ki >= expected - sd_binom and ki <= expected + sd_binom
                  else '#81c784' for ki in k]
        ax.bar(k, pmf, color=colors, width=0.8, edgecolor='white', linewidth=0.3)
        ax.axvline(expected, color='#1b5e20', linestyle='--', linewidth=1.5,
                   label=f'期待値 {expected:.1f}')
        ax.set_xlabel("発芽数（粒）", fontsize=11)
        ax.set_ylabel("確率", fontsize=11)
        ax.set_title(f"二項分布  n={n_seeds}, p={p_germ:.2f}", fontsize=12)
        ax.legend(fontsize=9)
        # X軸を適切な範囲に絞る
        lo = max(0, int(expected - 4*sd_binom))
        hi = min(n_seeds, int(expected + 4*sd_binom))
        ax.set_xlim(lo, hi)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.markdown("""
    <div class="concept-box">
    <b>農業試験での使いどころ</b><br>
    • 発芽率検定（品種 A vs B の発芽率に差があるか）<br>
    • 病害罹病株の割合比較<br>
    • n が大きく p が 0.5 付近 → 正規分布で近似可能（中心極限定理）<br>
    • p が 0 や 1 に近い → 正規近似は危険。GLM（ロジスティック回帰）を使う
    </div>
    """, unsafe_allow_html=True)

    # ── アークサイン変換セクション ──
    st.divider()
    st.subheader("分散分析で使う場合：アークサイン変換（角変換）")

    st.markdown("""
    <div class="warning-box">
    <b>なぜ変換が必要か？</b><br>
    割合データ（発芽率など）は 0〜1 の有界データ。
    分散分析（ANOVA）は残差が正規分布・等分散であることを前提とするが、
    割合データは <b>平均が端に近いほど分散が小さくなる</b>（不等分散）。
    → アークサイン変換で分散を安定させ、正規性に近づける。
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.markdown("#### 変換式")
        st.latex(r"y = \arcsin\!\left(\sqrt{p}\right)")
        st.markdown("""
- p：発芽率（0〜1）
- y：変換値（単位：ラジアン、0〜π/2）
- 変換後に分散分析を実施し、**結果の表示は元の %** に戻す
        """)
        st.markdown("#### Excelでの計算")
        st.code(
            "発芽率が小数（例：0.80）の場合\n"
            "  変換: =ASIN(SQRT(A2))\n"
            "  結果 ≈ 1.107 rad\n"
            "\n"
            "発芽率が % 表示（例：80）の場合\n"
            "  変換: =ASIN(SQRT(A2/100))\n"
            "\n"
            "逆変換（ラジアン → 割合）\n"
            "  =SIN(B2)^2",
            language="")

    with col_b:
        np.random.seed(42)
        true_ps = [0.1, 0.3, 0.5, 0.7, 0.9]
        colors_ps = ['#e53935', '#fb8c00', '#43a047', '#1e88e5', '#8e24aa']
        n_trial = 50

        fig2, axes = plt.subplots(1, 2, figsize=(8, 4))
        for p_true, col in zip(true_ps, colors_ps):
            samples = np.random.binomial(n_trial, p_true, size=100) / n_trial
            axes[0].hist(samples, bins=15, alpha=0.5, color=col,
                         label=f'p={p_true}', density=True)
            asin_samples = np.arcsin(np.sqrt(samples))
            axes[1].hist(asin_samples, bins=15, alpha=0.5, color=col,
                         label=f'p={p_true}', density=True)

        axes[0].set_title('変換前（割合データ）', fontsize=11)
        axes[0].set_xlabel('発芽率', fontsize=10)
        axes[0].set_ylabel('密度', fontsize=10)
        axes[0].legend(fontsize=7, title='真のp', title_fontsize=8)
        axes[1].set_title('変換後（arcsin√p）', fontsize=11)
        axes[1].set_xlabel('arcsin(√発芽率)  [rad]', fontsize=10)
        axes[1].set_ylabel('密度', fontsize=10)
        axes[1].legend(fontsize=7, title='真のp', title_fontsize=8)
        fig2.suptitle('アークサイン変換前後の分布比較（n=50）', fontsize=11)
        fig2.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)
        st.caption("変換後は各グループの分布幅（分散）がより均一になる")

    st.markdown("""
    <div class="concept-box">
    <b>実務上の判断基準</b>

    | 状況 | 推奨手法 |
    |------|---------|
    | p が 0.2〜0.8 の範囲、n が大 | 変換なし or 変換ありの ANOVA どちらも可 |
    | p が 0.2 未満または 0.8 超 | アークサイン変換して ANOVA |
    | p が 0 や 1 を含む、n が小 | GLM（ロジスティック回帰）を使う |

    アークサイン変換は古典的手法。現代統計では GLM が推奨されるが、農業試験の慣例として残っている。
    新人には「変換の目的＝等分散化」を理解させること。
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# TAB 3: ポアソン分布
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.subheader("ポアソン分布 — 塊茎腐敗数を例に")

    st.markdown("""
    <div class="concept-box">
    <b>ポアソン分布とは？</b><br>
    単位あたりの「まれな事象の発生数」の分布。<br>
    パラメータ：λ（平均発生数）。<b>平均＝分散</b> が成立するのが特徴。
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### パラメータ設定")
        lam = st.slider("平均腐敗塊茎数（個/株）", 0.1, 15.0, 2.0, step=0.1)

        st.metric("平均（λ）",  f"{lam:.1f} 個")
        st.metric("分散（＝λ）", f"{lam:.1f}")
        st.metric("標準偏差",   f"{np.sqrt(lam):.2f} 個")

        prob_zero = stats.poisson.pmf(0, mu=lam)
        st.metric("腐敗なし（0個）の確率", f"{prob_zero*100:.1f}%")

    with col2:
        k_max = max(20, int(lam + 5*np.sqrt(lam) + 2))
        k = np.arange(0, k_max + 1)
        pmf = stats.poisson.pmf(k, mu=lam)

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(k, pmf, color='#5c6bc0', alpha=0.75,
               edgecolor='white', linewidth=0.3)
        ax.axvline(lam, color='#1a237e', linestyle='--', linewidth=1.5,
                   label=f'λ = {lam:.1f}')
        ax.set_xlabel("腐敗塊茎数（個/株）", fontsize=11)
        ax.set_ylabel("確率", fontsize=11)
        ax.set_title(f"ポアソン分布  λ={lam:.1f}", fontsize=12)
        ax.legend(fontsize=9)
        display_max = min(k_max, int(lam + 4*np.sqrt(lam) + 3))
        ax.set_xlim(-0.5, display_max)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.markdown("""
    <div class="concept-box">
    <b>農業試験での使いどころ</b><br>
    • 塊茎腐敗数・ウイルス感染株数・害虫捕獲数<br>
    • λ が大きくなると正規分布に近づく<br>
    • <b>過分散</b>（分散＞平均）が多い → 負の二項分布や GLMM で対応<br>
    • 0 が多い（零過剰）場合は Zero-Inflated モデルを検討
    </div>
    """, unsafe_allow_html=True)

    # ── 対数変換セクション ──
    st.divider()
    st.subheader("分散分析で使う場合：対数変換")

    st.markdown("""
    <div class="warning-box">
    <b>なぜ変換が必要か？</b><br>
    カウントデータ（腐敗数など）は右に裾を引く正の歪み分布になりやすい。
    分散も平均に比例して大きくなる（等分散の仮定に違反）。
    → 対数変換により <b>右歪みを対称化</b>し、分散を安定させる。
    </div>
    """, unsafe_allow_html=True)

    col_c, col_d = st.columns([1, 2])
    with col_c:
        st.markdown("#### 変換式")
        st.latex(r"y = \log(x + 1)")
        st.markdown("""
- x：腐敗塊茎数（0 以上の整数）
- **+1 の理由**：x = 0 のとき log(0) = −∞ になるのを防ぐ
- 自然対数（ln）・常用対数（log₁₀）どちらも使われるが統一が必要
- 変換後に分散分析 → **結果の表示は元のスケール**（逆変換 = exp(y)−1）
        """)
        st.markdown("#### Excelでの計算")
        st.code(
            "自然対数変換（x=0 を含む場合）\n"
            "  変換: =LN(A2+1)\n"
            "\n"
            "常用対数変換（base 10）\n"
            "  変換: =LOG10(A2+1)\n"
            "\n"
            "逆変換（自然対数の場合）\n"
            "  =EXP(B2)-1\n"
            "\n"
            "逆変換（常用対数の場合）\n"
            "  =10^B2-1",
            language="")

    with col_d:
        np.random.seed(123)
        lam_demo = 3.0
        raw_counts = np.random.poisson(lam_demo, size=200)
        # 過分散を再現するため一部に大きな値を混在
        raw_counts = np.append(raw_counts,
                               np.random.negative_binomial(2, 0.3, size=50))
        log_counts = np.log1p(raw_counts)

        fig3, axes3 = plt.subplots(1, 2, figsize=(8, 4))

        axes3[0].hist(raw_counts, bins=range(0, int(raw_counts.max())+2),
                      color='#5c6bc0', alpha=0.75, edgecolor='white')
        axes3[0].set_title('変換前（腐敗塊茎数）', fontsize=11)
        axes3[0].set_xlabel('腐敗数（個/株）', fontsize=10)
        axes3[0].set_ylabel('頻度', fontsize=10)
        mean0, sd0 = raw_counts.mean(), raw_counts.std()
        axes3[0].axvline(mean0, color='#1a237e', linestyle='--', linewidth=1.5,
                         label=f'平均 {mean0:.1f}')
        axes3[0].legend(fontsize=8)

        axes3[1].hist(log_counts, bins=20, color='#26a69a', alpha=0.75,
                      edgecolor='white')
        axes3[1].set_title('変換後（log(x+1)）', fontsize=11)
        axes3[1].set_xlabel('log(腐敗数 + 1)', fontsize=10)
        axes3[1].set_ylabel('頻度', fontsize=10)
        mean1, sd1 = log_counts.mean(), log_counts.std()
        axes3[1].axvline(mean1, color='#004d40', linestyle='--', linewidth=1.5,
                         label=f'平均 {mean1:.2f}')
        axes3[1].legend(fontsize=8)

        fig3.suptitle('対数変換前後の分布比較（模擬データ）', fontsize=11)
        fig3.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)
        st.caption("右に裾を引く分布が、変換後に左右対称に近づく")

    st.markdown("""
    <div class="concept-box">
    <b>実務上の判断基準</b>

    | 状況 | 推奨手法 |
    |------|---------|
    | 右歪み、0 を含まない | log(x) 変換して ANOVA |
    | 0 を含む（腐敗なしの株がある） | log(x+1) 変換して ANOVA |
    | 0 が非常に多い（零過剰） | GLM（ポアソン/負の二項）または Zero-Inflated モデル |
    | 過分散が顕著 | GLM（負の二項分布）または GLMM |

    log 変換も古典的手法。0 の多いカウントデータには GLM の方が適切。
    </div>
    """, unsafe_allow_html=True)

    # 3分布比較
    st.divider()
    st.subheader("3 分布の比較まとめ")
    st.markdown("""
    | 分布 | データの型 | 農業例 | パラメータ | 注意点 |
    |------|-----------|--------|-----------|--------|
    | 正規分布 | 連続・無制限 | 収量、草丈 | μ, σ | 0・100付近で破綻 |
    | 二項分布 | 整数・0〜n | 発芽数、罹病株数 | n, p | p が端値なら GLM |
    | ポアソン分布 | 整数・0以上 | 腐敗数、虫数 | λ | 過分散に注意 |
    """)


# ═══════════════════════════════════════════════════════════════
# TAB 4: 仮説検定の用語
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.subheader("仮説検定の用語解説")

    terms = [
        ("帰無仮説（H₀）",
         "「差がない」「効果がない」という仮説。検定で棄却しようとする対象。\n\n"
         "例：「品種 A と品種 B の収量は同じである」"),
        ("対立仮説（H₁）",
         "帰無仮説が棄却されたときに採択される仮説。\n\n"
         "例：「品種 A と品種 B の収量は異なる」"),
        ("p 値",
         "帰無仮説が正しいと仮定したとき、観察された差（以上の差）が\n"
         "偶然に生じる確率。\n\n"
         "p < 0.05 → 5% 水準で有意（慣例的閾値であることに注意）"),
        ("有意水準（α）",
         "帰無仮説を棄却する基準となる確率。通常 0.05（5%）または 0.01（1%）。\n\n"
         "⚠️ α を小さくすると偽陰性（見落とし）が増える"),
        ("第一種の誤り（α 誤り）",
         "帰無仮説が正しいのに棄却してしまう誤り（偽陽性）。\n\n"
         "例：差がないのに「有意差あり」と判断 → 誤った品種推奨につながる"),
        ("第二種の誤り（β 誤り）",
         "帰無仮説が誤りなのに棄却できない誤り（偽陰性）。\n\n"
         "例：本当に差があるのに「差なし」と判断 → 優良品種を見逃す"),
        ("検出力（Power = 1−β）",
         "真の差を正しく検出できる確率。\n\n"
         "サンプルサイズを増やすほど検出力が上がる。実験計画の核心。"),
        ("多重比較の問題",
         "複数の組み合わせを同時に検定すると、偶然に有意差が出る確率が上昇する。\n\n"
         "品種比較では Dunnett 法（対照区 vs 各品種）や Tukey 法を使う。"),
    ]

    for term, explanation in terms:
        color = "#e8f4fd" if "誤り" not in term else "#fff3e0"
        border = "#1565c0" if "誤り" not in term else "#e65100"
        st.markdown(f"""
        <div style="background:{color}; border-left:4px solid {border};
                    padding:12px 16px; border-radius:4px; margin:8px 0;">
        <b>{term}</b><br>
        <span style="white-space:pre-line;">{explanation}</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("検定の流れ（農業試験の例）")
    st.markdown("""
    ```
    1. 研究仮説を設定
       「新品種 X は対照品種より収量が高い」

    2. 帰無仮説・対立仮説を設定
       H₀: μ_X = μ_対照
       H₁: μ_X ≠ μ_対照（両側）または μ_X > μ_対照（片側）

    3. 有意水準を決める（事前に！）
       α = 0.05

    4. 試験設計・データ収集
       反復数、ブロック構成 → 実験計画法へ

    5. 検定統計量を計算
       t 検定 / F 検定 / χ² 検定 など

    6. p 値を α と比較
       p < 0.05 → H₀ を棄却 → 「有意差あり」

    7. 結論（統計的有意性 ≠ 実用的重要性）
       差が有意でも、実際の収量差が農業的に意味あるかを判断
    ```
    """)

    st.markdown("""
    <div class="warning-box">
    <b>⚠️ よくある誤解</b><br>
    • p > 0.05 は「差がない証明」ではない → 「差を検出できなかった」<br>
    • p 値は効果の大きさを示さない → 効果量（Cohen's d 等）を合わせて報告<br>
    • 同じデータで何度も検定してはいけない（p-hacking）
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("農業統計研修 第1章 | 次回：実験計画法（RCBD・Latin Square）")
