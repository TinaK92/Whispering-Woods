import { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { fetchAddAnimal } from '../../redux/adoption';
import { toast } from 'react-toastify';

export const NewAnimal = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const [animal_name, setAnimal_name] = useState('');
  const [animal_age, setAnimal_age] = useState('');
  const [animal_color, setAnimal_color] = useState('');
  const [animal_breed, setAnimal_breed] = useState('');
  const [animal_bio, setAnimal_bio] = useState('');
  const [adoption_fee, setAdoption_fee] = useState('');
  const [image_url, setImage_url] = useState(null);
  const [formErrors, setFormErrors] = useState({});
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [hasSubmitted, setHasSubmitted] = useState(false);

  const user = useSelector((state) => state.session.user);

  useEffect(() => {
    const errors = {};
    if (animal_name.length < 3 || animal_name.length > 100) {
      errors.animal_name = 'Animal name must be between 3 and 100 characters';
    }
    if (!animal_age) {
      errors.animal_age = 'Animal age is required';
    }
    if (animal_color.length < 3 || animal_color.length > 255) {
      errors.animal_color = 'Color must be between 3 and 255 characters';
    }
    if (animal_breed.length < 5 || animal_breed.length > 255) {
      errors.animal_breed = 'Breed must be between 5 and 255 characters';
    }
    if (animal_bio.length < 10 || animal_bio.length > 1500) {
      errors.animal_bio = 'Bio must be between 10 and 1500 characters';
    }
    if (!adoption_fee || adoption_fee < 1) {
      errors.adoption_fee = 'Adoption fee must be greater than or equal to $1';
    }
    if (!image_url) {
      errors.image_url = 'Image is required';
    }

    setFormErrors(errors);
  }, [
    animal_name,
    animal_age,
    animal_color,
    animal_breed,
    animal_bio,
    adoption_fee,
    image_url,
    selectedCategories,
  ]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setHasSubmitted(true);

    if (Object.keys(formErrors).length > 0) {
      return;
    }

    const formData = new FormData();
    formData.append('user_id', user.id);
    formData.append('animal_name', animal_name);
    formData.append('animal_age', animal_age);
    formData.append('animal_color', animal_color);
    formData.append('animal_breed', animal_breed);
    formData.append('animal_bio', animal_bio);
    formData.append('adoption_fee', adoption_fee);
    formData.append('image', image_url);
    formData.append('categories', JSON.stringify(selectedCategories));

    const response = await dispatch(fetchAddAnimal(formData));

    if (response?.error) {
      setFormErrors(response.error);
    } else {
      toast.success('Animal has been created!');
      navigate('/adoptions');
    }
  };

  return (
    <form onSubmit={handleSubmit} encType="multipart/form-data">
      <div>
        <label>Animal Name</label>
        <input
          type="text"
          value={animal_name}
          onChange={(e) => setAnimal_name(e.target.value)}
        />
        {formErrors.animal_name && <p>{formErrors.animal_name}</p>}
      </div>

      <div>
        <label>Animal Age</label>
        <input
          type="text"
          value={animal_age}
          onChange={(e) => setAnimal_age(e.target.value)}
        />
        {formErrors.animal_age && <p>{formErrors.animal_age}</p>}
      </div>

      <div>
        <label>Animal Color</label>
        <input
          type="text"
          value={animal_color}
          onChange={(e) => setAnimal_color(e.target.value)}
        />
        {formErrors.animal_color && <p>{formErrors.animal_color}</p>}
      </div>

      <div>
        <label>Animal Breed</label>
        <input
          type="text"
          value={animal_breed}
          onChange={(e) => setAnimal_breed(e.target.value)}
        />
        {formErrors.animal_breed && <p>{formErrors.animal_breed}</p>}
      </div>

      <div>
        <label>Animal Bio</label>
        <textarea
          value={animal_bio}
          onChange={(e) => setAnimal_bio(e.target.value)}
        />
        {formErrors.animal_bio && <p>{formErrors.animal_bio}</p>}
      </div>

      <div>
        <label>Adoption Fee</label>
        <input
          type="number"
          value={adoption_fee}
          onChange={(e) => setAdoption_fee(e.target.value)}
        />
        {formErrors.adoption_fee && <p>{formErrors.adoption_fee}</p>}
      </div>

      <div>
        <label>Animal Image</label>
        <input
          type="file"
          onChange={(e) => setImage_url(e.target.files[0])}
        />
        {formErrors.image_url && <p>{formErrors.image_url}</p>}
      </div>

      {/* Future: Category checkboxes can go here */}

      <button type="submit">Submit</button>
    </form>
  );
};

export default NewAnimal;
