import { THEMES, useTheme } from "../context/ThemeContext";
import Icon from "./Icon";

const THEME_ICONS = {
  clair: "sun",
  sombre: "moon",
  sahel: "sahel",
};

export default function ThemeSwitch() {
  const { theme, cycleTheme } = useTheme();
  const current = THEMES.find((item) => item.id === theme) || THEMES[0];
  const iconName = THEME_ICONS[current.id] || "sun";

  return (
    <button
      type="button"
      className="theme-fab"
      onClick={cycleTheme}
      aria-label={`Thème ${current.label} — cliquer pour changer`}
      title={`Thème : ${current.label}`}
      data-theme-preview={current.id}
    >
      <Icon name={iconName} size={18} />
    </button>
  );
}
