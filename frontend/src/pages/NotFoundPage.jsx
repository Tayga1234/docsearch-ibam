import { Link } from "react-router-dom";
import EmptyState from "../components/EmptyState";

export default function NotFoundPage() {
  return (
    <section className="page">
      <EmptyState title="Page introuvable">
        <p>Cette adresse ne correspond à aucune vue de DocSearch.</p>
        <Link to="/" className="btn primary">
          Retour à la recherche
        </Link>
      </EmptyState>
    </section>
  );
}
