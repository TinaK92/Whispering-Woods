import { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { fetchCreateListing } from "../../redux/listing";
import { fetchAllSizes } from "../../redux/size";
import { fetchAllColors } from "../../redux/color";
import { addNewColor } from "../../redux/color";
import "./NewListing.css";

export const NewListing = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const user = useSelector((state) => state.session.user);
  const sizes = useSelector((state) => state.sizes.sizes);
  const colors = useSelector((state) => state.colors.colors);

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [basePrice, setBasePrice] = useState("");
  const [selectedSizes, setSelectedSizes] = useState([]);
  const [selectedColors, setSelectedColors] = useState([]);
  const [newColor, setNewColor] = useState("");
  const [colorError, setColorError] = useState(null);
  const [imageFiles, setImageFiles] = useState({});
  const [imageLoading, setImageLoading] = useState({});
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (!user || user.role !== "admin") {
      alert("You are not authorized to access this page.");
      window.location.href = "/";
    } else {
      dispatch(fetchAllColors());
      dispatch(fetchAllSizes());
    }
  }, [dispatch, user]);

  const validateForm = () => {
    const errors = {};
    if (!name.trim()) errors.name = "Name is required.";
    if (!description.trim()) errors.description = "Description is required.";
    if (!basePrice || isNaN(basePrice) || basePrice <= 0) {
      errors.basePrice = "Price must be a positive number.";
    }
    if (selectedSizes.length === 0) {
      errors.sizes = "At least one size must be selected.";
    }
    if (selectedColors.length === 0) {
      errors.colors = "At least one color must be selected.";
    }

    selectedColors.forEach((colorId) => {
      const images = imageFiles[colorId] || {};
      if (!images.front) {
        errors[
          `frontImage_${colorId}`
        ] = `Front image is required for color ID ${colorId}.`;
      }
      if (!images.back) {
        errors[
          `backImage_${colorId}`
        ] = `Back image is required for color ID ${colorId}.`;
      }
    });

    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    const formErrors = validateForm();
    if (Object.keys(formErrors).length > 0) {
      setErrors(formErrors);
      setIsSubmitting(false);
      return;
    }

    const formData = new FormData();
    formData.append("name", name);
    formData.append("description", description);
    formData.append("base_price", basePrice);
    selectedSizes.forEach((size) => formData.append("sizes", size));
    // 🔹 Fix: Append images correctly (without nested keys)
    selectedColors.forEach((colorId) => {
        if (imageFiles[colorId]?.front) {
            formData.append("front_image", imageFiles[colorId].front);
        }
        if (imageFiles[colorId]?.back) {
            formData.append("back_image", imageFiles[colorId].back);
        }
    });
    // Debugging Step 1: Log FormData contents
    for (let pair of formData.entries()) {
      console.log(`${pair[0]}:`, pair[1]);
    }

    console.log("FORM DATA ========", formData);


      const response = await dispatch(fetchCreateListing(formData));
      alert("Listing created successfully!");
      if (response.errors) {
        setErrors(response.errors)
      } else {
      setName("");
      setDescription("");
      setBasePrice("");
      setSelectedSizes([]);
      setSelectedColors([]);
      setImageFiles({});
      setErrors({});
      navigate("/listings");
      }
  };

  const handleSizeChange = (e) => {
    const { value, checked } = e.target;
    const sizeId = parseInt(value);

    if (checked) {
      setSelectedSizes((prev) => [...prev, sizeId]);
    } else {
      setSelectedSizes((prev) => prev.filter((id) => id !== sizeId));
    }
  };

  const handleColorChange = (e) => {
    const { value, checked } = e.target;
    const colorId = parseInt(value);

    if (checked) {
      setSelectedColors((prev) => [...prev, colorId]);
    } else {
      setSelectedColors((prev) => prev.filter((id) => id !== colorId));
      setImageFiles((prev) => {
        const updated = { ...prev };
        delete updated[colorId];
        return updated;
      });
    }
  };

  const handleImageChange = (colorId, type, file) => {
    setImageFiles((prev) => ({
      ...prev,
      [colorId]: {
        ...prev[colorId],
        [type]: file,
      },
    }));
  };

  const handleAddColor = async () => {
    setColorError(null);

    if (!newColor.trim()) {
      setColorError("Color name cannot be empty.");
      return;
    }

    try {
      const addedColor = await dispatch(addNewColor({ name: newColor }));
      setSelectedColors((prev) => [...prev, addedColor.id]); // Automatically select the new color
      setNewColor(""); // Reset the input field
      alert(`${addedColor.name} has been added and selected!`);
    } catch (error) {
      setColorError(error.message);
    }
  };

  if (!user || user.role !== "admin") {
    return null;
  }

  return (
    <div>
      <h1>Create New Listing</h1>
      <form onSubmit={handleSubmit} encType="multipart/form-data">
        <div>
          <label>Name</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          {errors.name && <p className="error">{errors.name}</p>}
        </div>
        <div>
          <label>Description</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
          {errors.description && <p className="error">{errors.description}</p>}
        </div>
        <div>
          <label>Base Price</label>
          <input
            type="text"
            id="basePrice"
            value={basePrice}
            onChange={(e) => setBasePrice(e.target.value)}
          />
          {errors.basePrice && <p className="error">{errors.basePrice}</p>}
        </div>
        <div>
          <label>Sizes</label>
          <div>
            {sizes.map((size) => (
              <div key={size.id}>
                <label>{size.name}</label>
                <input
                  type="checkbox"
                  value={size.id}
                  checked={selectedSizes.includes(size.id)}
                  onChange={handleSizeChange}
                />
              </div>
            ))}
          </div>
          {errors.sizes && <p className="error">{errors.sizes}</p>}
        </div>
        <div>
          <label>Colors</label>
          <div>
            {colors.map((color) => (
              <div key={color.id}>
                <label>{color.name}</label>
                <input
                  type="checkbox"
                  value={color.id}
                  checked={selectedColors.includes(color.id)}
                  onChange={handleColorChange}
                />
                {selectedColors.includes(color.id) && (
                  <div>
                    <label>Front Image</label>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={(e) =>
                        handleImageChange(color.id, "front", e.target.files[0])
                      }
                    />
                    {errors[`frontImage_${color.id}`] && (
                      <p className="error">
                        {errors[`frontImage_${color.id}`]}
                      </p>
                    )}
                    <label>Back Image</label>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={(e) =>
                        handleImageChange(color.id, "back", e.target.files[0])
                      }
                    />
                    {errors[`backImage_${color.id}`] && (
                      <p className="error">{errors[`backImage_${color.id}`]}</p>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
          {errors.colors && <p className="error">{errors.colors}</p>}
        </div>
        <div>
          <label>New Color</label>
          <input
            type="text"
            placeholder="Enter new color"
            value={newColor}
            onChange={(e) => setNewColor(e.target.value)}
          />
          <button type="button" onClick={handleAddColor}>
            Add Color
          </button>
          {colorError && <p className="error">{colorError}</p>}
        </div>
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Submitting..." : "Create Listing"}
        </button>
      </form>
    </div>
  );
};

export default NewListing;
