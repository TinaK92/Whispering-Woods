import { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { addNewColor } from '../../redux/color';
import { fetchAllColors } from '../../redux/color';
import { fetchCreateListing } from '../../redux/listing';
import { fetchAllSizes } from '../../redux/size';
import './NewListing.css';

export const NewListing = () => {
	const dispatch = useDispatch();
	const navigate = useNavigate();

	const [name, setName] = useState('');
	const [description, setDescription] = useState('');
	const [basePrice, setBasePrice] = useState('');
	const [selectedColor, setSelectedColor] = useState('');
	const [selectedSizes, setSelectedSizes] = useState([]);
	const [frontFile, setFrontFile] = useState(null);
	const [backFile, setBackFile] = useState(null);

	const user = useSelector((state) => state.session.user);
	const sizes = useSelector((state) => state.sizes.sizes);
	const colors = useSelector((state) => state.colors.colors);

	useEffect(() => {
		dispatch(fetchAllSizes());
		dispatch(fetchAllColors());
	}, [dispatch]);

	const handleSizeCheckboxChange = (e, sizeId) => {
		if (e.target.checked) {
			// If checked, add sizeId to the array
			setSelectedSizes((prev) => [...prev, sizeId]);
		} else {
			// If unchecked, remove sizeId
			setSelectedSizes((prev) => prev.filter((id) => id !== sizeId));
		}
	};

	const handleColorChange = (e) => {
		setSelectedColor(e.target.value);
	};

	const handleSubmit = async (e) => {
		e.preventDefault();

		const formData = new FormData();
		formData.append('name', name);
		formData.append('description', description);
		formData.append('base_price', basePrice);

		// Multiple sizes:
		selectedSizes.forEach((sizeId) => {
			formData.append('sizes', sizeId); // each appended as "sizes"
		});

		// Single color:
		formData.append('color', selectedColor);

		// Two images:
		if (frontFile) formData.append('front_image', frontFile);
		if (backFile) formData.append('back_image', backFile);

		// If you have a Redux thunk or similar for creation:
		const response = await dispatch(fetchCreateListing(formData));
		if (response.errors) {
			// handle or display errors
			console.log('Errors creating listing:', response.errors);
		} else {
			// success — maybe redirect
			console.log('Listing created successfully!', response.listing);
			navigate('/listings');
		}

		// For demo, just log the FormData keys & values:
		for (let pair of formData.entries()) {
			console.log(pair[0], pair[1]);
		}
	};

	return (
		<form
			onSubmit={handleSubmit}
			encType='multipart/form-data'
		>
			<h2>Create a New Listing</h2>

			<label>Listing Name</label>
			<input
				type='text'
				value={name}
				onChange={(e) => setName(e.target.value)}
				required
			/>

			<label>Description</label>
			<textarea
				value={description}
				onChange={(e) => setDescription(e.target.value)}
				required
			/>

			<label>Base Price</label>
			<input
				type='number'
				step='0.01'
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
							type='checkbox'
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
			<select
				value={selectedColor}
				onChange={handleColorChange}
				required
			>
				<option value=''>-- Select a color --</option>
				{colors?.map((color) => (
					<option
						key={color.id}
						value={color.id}
					>
						{color.name}
					</option>
				))}
			</select>

			{/* Two images: Front / Back */}
			<label>Front Image</label>
			<input
				type='file'
				accept='image/*'
				onChange={(e) => setFrontFile(e.target.files[0])}
				required
			/>

			<label>Back Image</label>
			<input
				type='file'
				accept='image/*'
				onChange={(e) => setBackFile(e.target.files[0])}
				required
			/>

			<button type='submit'>Create Listing</button>
		</form>
	);
};

export default NewListing;
