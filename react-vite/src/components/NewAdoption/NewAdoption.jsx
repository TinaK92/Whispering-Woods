import { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { fetchAddAnimal } from '../../redux/adoption';

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
            errors.animal_name = "Animal age must be between 3 and 100 characters";
        }
        if (animal_age.length <= 0) {
            errors.animals_age = 'Age must not be blank, you can use numbers and characters';
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
        if (adoption_fee < 1) {
            errors.adoption_fee = 'Adoption fee must be greater than or equal to $1';
        }
        if (!animal_name) errors.animals_name = 'Animals name is required';
        if (!animal_age) errors.animal_name = 'Animals age is required';
        if (!animal_color) errors.animal_color = 'Animals color is required';
        if (!animal_breed) errors.animal_breed = 'Animals breed is required';
        if (!animal_bio) errors.animal_bio = 'Animals bio is required';
        if (!adoption_fee) errors.adoption_fee = 'Adoption fee is required';
        setFormErrors(errors);
    }, [animal_name, animal_age, animal_color, animal_breed, animal_bio, adoption_fee, image_url, selectedCategories]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setHasSubmitted(true);

        if (Object.keys(formErrors).length > 0) {
            return;
        }

        const newAnimal = {
            user_id: user.id,
            animal_name: animal_name,
            animal_age: animal_age,
            animal_color: animal_color,
            animal_breed: animal_breed,
            animal_bio: animal_bio,
            adoption_fee: adoption_fee,
            image_url: image_url,
            categories: selectedCategories
        };

        const response = await dispatch(fetchAddAnimal(newAnimal));
        if (response?.error) {
            setFormErrors(response.error);
        } else {
            navigate('/adoptions');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>Animal Name</label>
                <input type="text" value={animal_name} onChange={(e) => setAnimalName(e.target.value)} />
                {formErrors.animal_name && <p>{formErrors.animal_name}</p>}
            </div>

            <div>
                <label>Animal Age</label>
                <input type="number" value={animal_age} onChange={(e) => setAnimalAge(e.target.value)} />
                {formErrors.animal_age && <p>{formErrors.animal_age}</p>}
            </div>

            <div>
                <label>Animal Color</label>
                <input type="text" value={animal_color} onChange={(e) => setAnimalColor(e.target.value)} />
                {formErrors.animal_color && <p>{formErrors.animal_color}</p>}
            </div>

            <div>
                <label>Animal Breed</label>
                <input type="text" value={animal_breed} onChange={(e) => setAnimalBreed(e.target.value)} />
                {formErrors.animal_breed && <p>{formErrors.animal_breed}</p>}
            </div>

            <div>
                <label>Animal Bio</label>
                <textarea value={animal_bio} onChange={(e) => setAnimalBio(e.target.value)} />
                {formErrors.animal_bio && <p>{formErrors.animal_bio}</p>}
            </div>

            <div>
                <label>Adoption Fee</label>
                <input type="number" value={adoption_fee} onChange={(e) => setAdoptionFee(e.target.value)} />
                {formErrors.adoption_fee && <p>{formErrors.adoption_fee}</p>}
            </div>

            <div>
                <label>Animal Image</label>
                <input type="file" onChange={(e) => setImageUrl(e.target.files[0])} />
                {formErrors.image_url && <p>{formErrors.image_url}</p>}
            </div>

            <button type="submit">Submit</button>
        </form>
    )
}

export default NewAnimal;