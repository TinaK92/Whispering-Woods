import { useSelector, useDispatch } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import { fetchAllListings } from "../../redux/listing";
import { useEffect } from "react";

import "./Listings.css";

export const Listings = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const user = useSelector((state) => state.session.user);
  const listings = useSelector((state) => [
    ...(state.listings?.AllListings || []),
  ]);

  const fullState = useSelector((state) => state);
  console.log("Full Redux state in component:", fullState);

  useEffect(() => {
    if (listings.length === 0) {
      dispatch(fetchAllListings());
    }
  }, [dispatch, listings.length]);

  const handleNavigate = (id) => {
    navigate(`/listings/${id}`)
  } 

  return (
    <div>
      <div>
        <img className="logo-image" src="/images/IMG_6714.JPG" />
      </div>
      <div className="mission-statement">
        <h1>Our Merchandise</h1>
        <p>
          Every purchase made directly supports Whispering Woods Animal Safe
          Haven and the animals we care for. All profits go towards providing
          essential resources, including food, medical care, and shelter, to
          animals in need. Your support helps us continue our mission of
          offering love, compassion, and a voice to every animal, no matter
          their size or background. Together, we can make a difference in the
          lives of countless animals, ensuring they receive the care and comfort
          they deserve. Thank you for helping us save lives!
        </p>
      </div>
      <div>
        {user?.role === "admin" && <Link to="/listings/new">Add New Item</Link>}
      </div>
      <div>
        <h2>Merchandise</h2>
        <div className="listings-container">
          {listings.length > 0 ? (
            listings.map((listing) => (
              <div key={listing.id} className="listing-card">
                <h3>{listing.name}</h3>
                <img
                  src={listing.front_image}
                  alt={listing.name}
                  className="listing-image"
                />
                <p>{listing.description}</p>
                <p>Price: ${listing.base_price}</p>
                <button 
                  onClick={() => handleNavigate(listing.id)}
                >
                  View Details
                </button>
              </div>
            ))
          ) : (
            <p>Loading merchandise or no listings available.</p> // Prevents crashing
          )}
        </div>
      </div>
    </div>
  );
};

export default Listings;
