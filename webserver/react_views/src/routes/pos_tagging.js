import { Link } from "react-router-dom";

export default function POSTagging() {
  return (
    <div>
      <h1>POS tagging</h1>
      <nav
        style={{
          borderBottom: "solid 1px",
          paddingBottom: "1rem",
        }}
      >
        <Link to="/">Home</Link> |{" "}
        <Link to="/postagging">POS tagging</Link> |{" "}
      </nav>
    </div>
  );
}
