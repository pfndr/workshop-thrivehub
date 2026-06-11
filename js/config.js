// PF Brand colors (per pathfinder-foundry-brand-mark-guide.md)
const ACCENT = "#FFCC64";       // PF Yellow — accent text, dot icon
const ACCENT_DIM = "rgba(255,204,100,0.18)";
const ACCENT_SOFT = "rgba(255,204,100,0.08)";
const BG = "#0f0f0f";
const PF_DARK = "#272727";
const TEXT = "#f5f5f5";
const TEXT_MUTED = "#a8a8a8";
const RED = "#ef4444";
const RED_DIM = "rgba(239,68,68,0.12)";
const GREEN = "#22c55e";
const GREEN_DIM = "rgba(34,197,94,0.12)";
const WARN = "#f59e0b";

const FONT_STACK =
  "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Roboto, sans-serif";
const TEXT_DIM    = "rgba(245,245,245,0.55)";
const CARD_BG     = "rgba(255,255,255,0.04)";   // card backgrounds (browser chrome, panels)
const CARD_BORDER = "rgba(255,255,255,0.10)";   // card borders

const SERIF_ITALIC =
  "'Baskerville', 'Baskerville Old Face', Garamond, Georgia, 'Times New Roman', serif";

// LoFi Music Library (HoliznaCC0 · CC0 1.0 Universal)
// Source: https://freemusicarchive.org/music/holiznacc0/public-domain-lofi
const LOFI_TRACKS = [
  "01-HoliznaCC0-Bubbles.mp3",
  "02-HoliznaCC0-Peaceful-Drift.mp3",
  "03-HoliznaCC0-Going-_Home_.mp3",
  "04-HoliznaCC0-Warm-Fuzz.mp3",
  "05-HoliznaCC0-Color-Of-A-Soul.mp3",
  "06-HoliznaCC0-Ode-To-Forgetting.mp3",
  "07-HoliznaCC0-Saturation.mp3",
  "08-HoliznaCC0-Wave-Maker.mp3",
  "09-HoliznaCC0-Complicated-Feelings.mp3",
  "10-HoliznaCC0-Wetlands.mp3",
  "11-HoliznaCC0-Dreamshifter.mp3",
  "12-HoliznaCC0-Dreamy-Reverie.mp3",
  "13-HoliznaCC0-Ease-into-Night.mp3",
  "14-HoliznaCC0-Infinite-Echoes.mp3",
  "15-HoliznaCC0-Into-The-Mist.mp3",
  "16-HoliznaCC0-Lucid.mp3",
  "17-HoliznaCC0-Never-Sleeping.mp3",
];
const LOFI_DIR = "./music/"; // run scripts/setup-music.sh once to symlink the canonical _assets/music here
const MUSIC_ATTRIBUTION_URL =
  "https://freemusicarchive.org/music/holiznacc0/public-domain-lofi";

// QR sources (paths relative to index.html)
const QR_SRC = {
  // Bespoke per-workshop access QR for the ProtoVibing app (yellow on transparent, no CSS filters)
  protovibingAccess: "./images/qr-protovibing-access.png",
  workshopFeedback: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAYwAAAGMCAYAAADJOZVKAAAH30lEQVR4nO3cwXHcRhRFUcLFkBSSw1JIzmm89Yp1IbPJ/4lzAhj1YEDd6s17ewMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC+2nX6H3j98/fr9L/xJNev39fm53/3/E9z+vea9vynvZ/bXYd/379OfjgAP4dgAJAIBgCJYACQCAYAiWAAkAgGAIlgAJAIBgCJYACQCAYAyfvbMNO2bk7bvh10+vx3P3/a+3P6/Hc/f/vznHaep21tuWEAkAgGAIlgAJAIBgCJYACQCAYAiWAAkAgGAIlgAJAIBgCJYACwc0tq+9bK9q2b7VtD07abnnb+aaZ932vY38tdbhgAJIIBQCIYACSCAUAiGAAkggFAIhgAJIIBQCIYACSCAUAiGAA8Y0uKXVs6p8+zfVvp9PmnfT67uGEAkAgGAIlgAJAIBgCJYACQCAYAiWAAkAgGAIlgAJAIBgCJYACQ2JLif5m2xbR9q2ra87QNxX+5YQCQCAYAiWAAkAgGAIlgAJAIBgCJYACQCAYAiWAAkAgGAIlgAPCMLSlbNz/b6e2mu+5+/unzT/v8abaffxo3DAASwQAgEQwAEsEAIBEMABLBACARDAASwQAgEQwAEsEAIBEMAHZuSZ3eAmLXNpHP/9mff5f/H76XGwYAiWAAkAgGAIlgAJAIBgCJYACQCAYAiWAAkAgGAIlgAJAIBgDJ0d0Xvt/27Z1p20TTznPa6e/LLm4YACSCAUAiGAAkggFAIhgAJIIBQCIYACSCAUAiGAAkggFAIhgAJMd3YqZt9Uw7//btoKc9n+3P867tz/+0a9jzP30eNwwAEsEAIBEMABLBACARDAASwQAgEQwAEsEAIBEMABLBACARDACSUbtNf2LaltG0Laxp20Hbnw8fsz31vWxJATCCYACQCAYAiWAAkAgGAIlgAJAIBgCJYACQCAYAiWAAkAgGAMn728O2iU6fZ/uWjuf5uWyXfa/tz+c17P13wwAgEQwAEsEAIBEMABLBACARDAASwQAgEQwAEsEAIBEMABLBAGDGltRpp7d3nraFNc32LaZpv9e05zNt62n7/yenuWEAkAgGAIlgAJAIBgCJYACQCAYAiWAAkAgGAIlgAJAIBgCJYACQjNpx+QlbK9u3Zbaff/tW1bTnOW3rabvXsC2vu9wwAEgEA4BEMABIBAOARDAASAQDgEQwAEgEA4BEMABIBAOARDAASEbtlPyJads7d03bijntaVtM00x73/xeu35fNwwAEsEAIBEMABLBACARDAASwQAgEQwAEsEAIBEMABLBACARDACS62lbMae3VqZ937tObzdN2zJ62hbW9t/X39fHbEkBMIJgAJAIBgCJYACQCAYAiWAAkAgGAIlgAJAIBgCJYACQCAYAyepdn4mmbb/ws7ehtpu2PTXtPHfZkgJgBMEAIBEMABLBACARDAASwQAgEQwAEsEAIBEMABLBACARDACS97dhpm3vTNuWOb1lNG0radp57pr2e9017XnetX2r7Rp2fjcMABLBACARDAASwQAgEQwAEsEAIBEMABLBACARDAASwQAgEQwAkuM7JdO2jKZtE23/vtO2jKad567tv9ddT9uqeg17f+5ywwAgEQwAEsEAIBEMABLBACARDAASwQAgEQwAEsEAIBEMABLBACAZtSvzFbZv15y2fRtn2u87bdtq+/M8bdqW12vYVpgbBgCJYACQCAYAiWAAkAgGAIlgAJAIBgCJYACQCAYAiWAAkAgGAMnjtqTuetpW0uktmrumfd9p20rTzj/t/Znmtfz5u2EAkAgGAIlgAJAIBgCJYACQCAYAiWAAkAgGAIlgAJAIBgCJYACQHN992b6dcte0raHt20SnbX9/nvZ7Pe39eR1+H+5ywwAgEQwAEsEAIBEMABLBACARDAASwQAgEQwAEsEAIBEMABLBACAZtaPD59u+HfS0raTT33fa55/m/J/LDQOARDAASAQDgEQwAEgEA4BEMABIBAOARDAASAQDgEQwAEgEA4Dk/e2w7ds+00zbunna8zn9Pm///O1bSaefz7X879cNA4BEMABIBAOARDAASAQDgEQwAEgEA4BEMABIBAOARDAASAQDgBlbUk/bWtm+XfO0raFpn/800/7ep21VXcOejxsGAIlgAJAIBgCJYACQCAYAiWAAkAgGAIlgAJAIBgCJYACQCAYAO7ek7pq21TNt+2XaVtVp29+H7dtW057/Xaef/zXs7+UuNwwAEsEAIBEMABLBACARDAASwQAgEQwAEsEAIBEMABLBACARDACesSXFru2a01s9d03bYpq2PXXXtPNs9xr2PN0wAEgEA4BEMABIBAOARDAASAQDgEQwAEgEA4BEMABIBAOARDAASGxJ8aVbSXzv8/f7fszz+ZgbBgCJYACQCAYAiWAAkAgGAIlgAJAIBgCJYACQCAYAiWAAkAgGAM/Ykrp+/b6++wxPdvr53932mfY+3D3P6S2j0+d52vtwDft9T3PDACARDAASwQAgEQwAEsEAIBEMABLBACARDAASwQAgEQwAEsEAYOeW1PatlWmmbe84z8/eMrKF9bmmnccNA4BEMABIBAOARDAASAQDgEQwAEgEA4BEMABIBAOARDAASAQDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOBtpn8B68y0Wg8WPCoAAAAASUVORK5CYII=",
};

const MONO =
  "ui-monospace, SFMono-Regular, Menlo, monospace"; // browser chrome address bar
