import { useSelector, useDispatch } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import {
  fetchAllAnimals,
  fetchDeleteAnimal,
  fetchGetAAnimal,
  fetchUpdateAnimal,
} from "../../redux/adoption";
import { useEffect } from "react";

export const Adoptions = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const user = useSelector((state) => state.session.user);
  const adoptions = useSelector((state) => [
    ...(state.adoptions?.AllAnimals || []),
  ]);

  useEffect(() => {
    dispatch(fetchAllAnimals());
  }, [dispatch]);

  const handleNavigate = (id) => {
    dispatch(fetchGetAAnimal(id));
    navigate(`/adoptions/${id}`);
  };

  const handleDelete = (id) => {
    dispatch(fetchDeleteAnimal(id));
  };

  return (
    <div>
      <div>
        {user?.role === "admin" && (
          <Link to="/adoptions/new">Add New Animal</Link>
        )}
      </div>
      <div className="title">
        <h2>Adoption</h2>
      </div>
      <div className="adoption-details">
        <p className="adoption-description">Animals Available for Adoption!</p>
      </div>
      <div className="adoptions-container">
        {adoptions.length > 0 ? (
          adoptions.map((adoption) => (
            <div key={adoption.id} className="adoption-card">
              <h3>{adoption.animal_name}</h3>
              <img
                src={adoption.image_url}
                alt={adoption.animal_name}
                className="animal-image"
              />
              <button onClick={() => handleNavigate(adoption.id)}>
                View Details
              </button>
            </div>
          ))
        ) : (
          <p>Loading animals available for adoption.</p>
        )}
      </div>
    </div>
  );
};


export default Adoptions;