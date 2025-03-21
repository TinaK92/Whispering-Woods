import { Link } from "react-router-dom";
import ProfileButton from "./ProfileButton";
import "./Navigation.css";
import { FaShoppingCart } from "react-icons/fa";

function Navigation() {
  return (
    <div className="nav-links">
      <div>
        <Link to="/">Whispering Woods</Link>
      </div>
      <div>
        <Link to="/">Home</Link>
      </div>
      <div>
        <Link to="/adoptions">Adopt</Link>
      </div>
      <div>
        <Link to="/listings">Shop</Link>
      </div>
      <div>
        <Link>Donate</Link>
      </div>
      <div className="profile-div">
        <ProfileButton />
      </div>
      <Link to="/current/shopping-cart">
        <FaShoppingCart />
      </Link>
    </div>
  );
}

export default Navigation;
