import listingsReducer, { fetchGetListing } from "../../redux/listing";
import { useSelector, useDispatch } from "react-redux";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { fetchUpdateListing } from "../../redux/listing";
import { fetchAllSizes } from "../../redux/size";
import { fetchAllColors } from "../../redux/color";


export const EditListing = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { id } = useParams();

  // Get the details of the listing using state
  const listing = useSelector((state) => state.listings.selectedListing);
  const sizes = useSelector((state) => state.sizes.sizes);
  const colors = useSelector((state) => state.colors.colors);

  // Local state for form fields
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [basePrice, setBasePrice] = useState("");
  const [selectedColor, setSelectedColor] = useState("");
  const [selectedSizes, setSelectedSizes] = useState([]);
  const [frontFile, setFrontFile] = useState(null);
  const [backFile, setBackFile] = useState(null);
  const [errors, setErrors] = useState({});

  // Fetch listing details and available sizes and colors
  useEffect(() => {
    dispatch(fetchGetListing(id));
    dispatch(fetchAllSizes());
    dispatch(fetchAllColors());
  }, [dispatch, id]);

  // Update form state when listing is fetched
  useEffect(() => {
    if (!listing) return;
  
    setName((prev) => (prev === "" ? listing.name : prev));
    setDescription((prev) => (prev === "" ? listing.description : prev));
    setBasePrice((prev) => (prev === "" ? listing.base_price : prev));
    setSelectedColor((prev) => (prev === "" ? listing.color_id : prev));
    setSelectedSizes((prev) =>
      prev.length === 0 ? listing.sizes?.map((size) => size.id) || [] : prev
    );
  }, [listing]);

  const handleSizeCheckboxChange = (e, sizeId) => {
    if (e.target.checked) {
      setSelectedSizes((prev) => [...prev, sizeId]);
    } else {
      setSelectedSizes((prev) => prev.filter((id) => id !== sizeId));
    }
  };

  const handleColorChange = (e) => {
    setSelectedColor(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("name", name);
    formData.append("description", description);
    formData.append("base_price", basePrice);
    formData.append("color", selectedColor);

    // Add multiple sizes
    selectedSizes.forEach((sizeId) => {
      formData.append("sizes", sizeId);
    });

    // Check if new files are selected before appending
    if (frontFile) formData.append("front_image", frontFile);
    if (backFile) formData.append("back_image", backFile);

    // Dispatch update action
    const response = await dispatch(fetchUpdateListing(id, formData));

    if (response.errors) {
        setErrors(response.errors);
        console.log("Errors updating listing:", response.errors);
      } else {
        console.log("Listing updated successfully!");
        navigate("/listings");
      }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Edit Listing</h2>
      <label>Listing Name</label>
      <input 
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      ></input>
      <label>Description</label>
      <input 
        type="text"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        required
        ></input>
        <label>Base Price</label>
      <input
        type="number"
        step="0.01"
        value={basePrice}
        onChange={(e) => setBasePrice(e.target.value)}
        required
      />

      {/* Multiple sizes */}
      <label>Sizes</label>
      {sizes.map((size) => (
        <div key={size.id}>
          <label>
            <input
              type="checkbox"
              value={size.id}
              checked={selectedSizes.includes(size.id)}
              onChange={(e) => handleSizeCheckboxChange(e, size.id)}
            />
            {size.name}
          </label>
        </div>
      ))}

      {/* Single color */}
      <label>Color</label>
      <select value={selectedColor} onChange={handleColorChange} required>
        <option value="">-- Select a color --</option>
        {colors?.map((color) => (
          <option key={color.id} value={color.id}>
            {color.name}
          </option>
        ))}
      </select>

      {/* Two images: Front / Back */}
      <label>Front Image (optional)</label>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFrontFile(e.target.files[0])}
      />

      <label>Back Image (optional)</label>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setBackFile(e.target.files[0])}
      />

      <button type="submit">Update Listing</button>
    </form>
  );
};

export default EditListing;
