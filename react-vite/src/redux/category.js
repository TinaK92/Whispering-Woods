const GET_ALL_CATEGORIES = 'categories/GET_ALL_CATEGORIES';

const getAllCategories = (categories) => {
	return {
		type: GET_ALL_CATEGORIES,
		payload: categories,
	};
};

export const fetchAllCategories = () => async (dispatch) => {
	const response = await fetch('/api/categories/all');
	if (response.ok) {
		const categories = await response.json();
		dispatch(getAllCategories(categories));
		return categories;
	}
};

const initialState = {
	categories: [],
};

export default function categoryReducer(state = initialState, action) {
	switch (action.type) {
		case GET_ALL_CATEGORIES:
			return { ...state, categories: action.payload };
		default:
			return state;
	}
}