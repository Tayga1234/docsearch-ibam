export const ICONS = {
  eye: ["M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7Z", "M12 15.2a3.2 3.2 0 1 0 0-6.4 3.2 3.2 0 0 0 0 6.4Z"],
  trash: ["M4 7h16", "M9 7V4h6v3", "M6 7l1 13h10l1-13", "M10 11v6", "M14 11v6"],
  download: ["M12 3v12", "M8 11l4 4 4-4", "M5 21h14"],
  back: ["M15 6l-6 6 6 6", "M9 12h11"],
  folder: ["M3 7h6l2 2h10v10H3z"],
  upload: ["M12 16V5", "M8 9l4-4 4 4", "M5 21h14"],
  rebuild: ["M4 4v6h6", "M20 20v-6h-6", "M20.5 9A8 8 0 0 0 7 6.3L4 10", "M3.5 15A8 8 0 0 0 17 17.7L20 14"],
  sun: [
    "M12 17.5a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11Z",
    "M12 2.5v2",
    "M12 19.5v2",
    "M2.5 12h2",
    "M19.5 12h2",
    "M5.05 5.05l1.4 1.4",
    "M17.55 17.55l1.4 1.4",
    "M5.05 18.95l1.4-1.4",
    "M17.55 6.45l1.4-1.4",
  ],
  moon: ["M20.5 14.2A7.8 7.8 0 0 1 9.8 3.5 8.2 8.2 0 1 0 20.5 14.2Z"],
  sahel: [
    "M4 17.5h16",
    "M6.5 17.5c1.2-3.2 2.8-5.2 5.5-5.2s4.3 2 5.5 5.2",
    "M12 8.2a2.4 2.4 0 1 0 0-4.8 2.4 2.4 0 0 0 0 4.8Z",
  ],
};

export default function Icon({ name, size = 18 }) {
  const paths = ICONS[name] || [];
  return (
    <svg viewBox="0 0 24 24" width={size} height={size} aria-hidden="true">
      {paths.map((d) => (
        <path
          key={d}
          d={d}
          fill="none"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      ))}
    </svg>
  );
}
