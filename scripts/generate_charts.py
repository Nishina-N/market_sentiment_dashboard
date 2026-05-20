#!/usr/bin/env python3
"""Generate chart PNGs for market-dashboard.html using yfinance + mplfinance."""
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).parent.parent
CHARTS_DIR = ROOT / "charts"
CHARTS_DIR.mkdir(exist_ok=True)

BG    = '#F5F3EF'
BORD  = '#D6D1C8'
INK   = '#2A2720'
MUTED = '#7A7468'
UP    = '#2D7A4F'
DOWN  = '#B84040'

MPSTYLE = mpf.make_mpf_style(
    base_mpf_style='yahoo',
    marketcolors=mpf.make_marketcolors(
        up=UP, down=DOWN,
        edge={'up': UP, 'down': DOWN},
        wick={'up': UP, 'down': DOWN},
        volume={'up': UP, 'down': DOWN},
        ohlc='i',
    ),
    facecolor=BG,
    edgecolor=BORD,
    figcolor=BG,
    gridcolor=BORD,
    gridstyle='-',
    gridaxis='both',
    rc={
        'axes.labelcolor': MUTED,
        'xtick.color': MUTED,
        'ytick.color': MUTED,
        'axes.edgecolor': BORD,
        'font.size': 9,
    },
)

FIGSIZE = (9, 6)
DPI = 120
PERIOD = "6mo"


def fetch(ticker: str) -> pd.DataFrame:
    df = yf.download(ticker, period=PERIOD, interval="1d",
                     auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.index = pd.DatetimeIndex(df.index).tz_localize(None)
    return df


def save_candle(filename: str, df: pd.DataFrame, volume: bool = True) -> None:
    mpf.plot(
        df, type='candle', style=MPSTYLE,
        figsize=FIGSIZE, volume=volume,
        tight_layout=True,
        savefig=dict(fname=CHARTS_DIR / filename, dpi=DPI,
                     bbox_inches='tight', facecolor=BG),
        warn_too_much_data=1000,
    )


def save_line(filename: str, df: pd.DataFrame) -> None:
    mpf.plot(
        df, type='line', style=MPSTYLE,
        figsize=FIGSIZE, volume=False,
        tight_layout=True,
        savefig=dict(fname=CHARTS_DIR / filename, dpi=DPI,
                     bbox_inches='tight', facecolor=BG),
        warn_too_much_data=1000,
    )


def save_ratio(filename: str, df1: pd.DataFrame, df2: pd.DataFrame,
               label: str) -> None:
    ratio = df1['Close'] / df2['Close']

    fig, ax = plt.subplots(figsize=FIGSIZE, facecolor=BG)
    ax.set_facecolor(BG)
    ax.plot(ratio.index, ratio.values, color=INK, linewidth=1.5, label=label)
    ax.legend(loc='upper left', fontsize=9, framealpha=0)
    ax.tick_params(colors=MUTED, labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor(BORD)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate()
    ax.grid(color=BORD, linestyle='-', linewidth=0.5)
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / filename, dpi=DPI, bbox_inches='tight', facecolor=BG)
    plt.close(fig)


def main() -> None:
    print("Generating charts...")

    save_candle("qqq.png", fetch("QQQ"))
    print("  qqq.png")

    save_candle("spy.png", fetch("SPY"))
    print("  spy.png")

    save_candle("iwm.png", fetch("IWM"))
    print("  iwm.png")

    save_candle("dia.png", fetch("DIA"))
    print("  dia.png")

    save_candle("smh.png", fetch("SMH"))
    print("  smh.png")

    save_line("vix.png", fetch("^VIX"))
    print("  vix.png")

    save_line("us10y.png", fetch("^TNX"))
    print("  us10y.png")

    save_ratio("spx_rut.png", fetch("^GSPC"), fetch("^RUT"), "SPX/RUT")
    print("  spx_rut.png")

    save_candle("xlk.png", fetch("XLK"))
    print("  xlk.png")

    save_candle("xlp.png", fetch("XLP"))
    print("  xlp.png")

    save_candle("xle.png", fetch("XLE"))
    print("  xle.png")

    save_candle("soxx.png", fetch("SOXX"))
    print("  soxx.png")

    save_candle("xly.png", fetch("XLY"))
    print("  xly.png")

    save_candle("xlv.png", fetch("XLV"))
    print("  xlv.png")

    save_candle("xlb.png", fetch("XLB"))
    print("  xlb.png")

    save_candle("xlu.png", fetch("XLU"))
    print("  xlu.png")

    save_candle("xli.png", fetch("XLI"))
    print("  xli.png")

    save_candle("xlc.png", fetch("XLC"))
    print("  xlc.png")

    save_candle("xlre.png", fetch("XLRE"))
    print("  xlre.png")

    save_candle("xlf.png", fetch("XLF"))
    print("  xlf.png")

    meta = {"updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    (CHARTS_DIR / "meta.json").write_text(json.dumps(meta))
    print(f"Done. Updated at {meta['updated_at']}")


if __name__ == "__main__":
    main()
