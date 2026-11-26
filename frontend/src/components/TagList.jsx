export default function TagList({ tags, onTagClick }) {
  if (!tags?.length) return null;

  return (
    <div className="tag-list">
      {tags.map((tag) =>
        onTagClick ? (
          <button
            key={tag}
            type="button"
            className="tag tag-btn"
            onClick={(event) => {
              event.stopPropagation();
              onTagClick(tag);
            }}
          >
            {tag}
          </button>
        ) : (
          <span key={tag} className="tag">
            {tag}
          </span>
        )
      )}
    </div>
  );
}
