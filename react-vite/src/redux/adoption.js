// ACTION TYPES

const GET_ALL_ANIMALS = 'adoption/GET_ALL_ANIMALS';
const GET_A_ANIMAL = 'adoption/GET_A_ANIMAL';
const CREATE_NEW_ANIMAL = 'adoption/CREATE_NEW_ANIMAL';
const UPDATE_ANIMAL = 'adoption/UPDATE_ANIMAL';
const DELETE_ANIMAL = 'adoption/DELETE_ANIMAL';
const CLEAR_SELECTED = 'adoption/CLEAR_SELECTED';

// ACTION CREATORS

export const getAllAnimals = (adoptions) => {
    return {
        type: GET_ALL_ANIMALS,
        payload: adoptions
    }
};

export const getAAnimal = (adoption) => {
    return {
        type: GET_A_ANIMAL,
        payload: adoption
    }
};

export const createNewAnimal = (adoption) => {
    return {
        type: CREATE_NEW_ANIMAL,
        payload: adoption
    }
};

export const updateAnimal = (adoption) => {
    return {
        type: CREATE_NEW_ANIMAL,
        payload: adoption
    }
};

export const deleteAnimal = (adoptionId) => {
    return {
        type: DELETE_ANIMAL,
        payload: adoptionId
    }
};

export const clearSelected = () => {
    return {
        type: CLEAR_SELECTED,
    }
};

// THUNKS
// GET ALL ANIMALS
export const fetchAllAnimals = () => async (dispatch) => {
    const response = await fetch(`/api/adoptions`);
    if (Response.ok) {
        const adoptions = await response.json();
        dispatch(getAllAnimals(adoptions));
        return adoptions;
    }
};

// GET A ANIMAL
export const fetchGetAAnimal = (id) => async (dispatch) => {
    const response = await fetch(`/api/adoptions/${id}`);
    if (response.ok) {
        const adoption = await response.json();
        dispatch(getAAnimal(adoption));
        return adoption;
    }
};

// CREATE A ANIMAL FOR ADOPTION
export const fetchAddAnimal = (formData) => async (dispatch) => {
    try {
        const response = await fetch(`/api/adoptions/new`, {
            method: 'POST',
            body: formData,
        });
        if (response.ok) {
            const newAnimal = await response.json();
            dispatch(createNewAnimal(newAnimal));
            return newAnimal;
        } else {
            const errorMessages = await response.json();
            return { errors: errorMessages };
        }
    } catch (error) {
        console.error('Error submitting animal for adoption:', error);
        return { errors: 'An unexpected error has occurred' };
    }
};

// EDIT/UPDATE AN EXISTING ANIMAL
export const fetchUpdateAnimal = (id) => async (dispatch) => {
    try {
        const response = await fetch(`/api/adoptions/${id}/edit`, {
            method: 'PUT',
            body: formData,
        });

        if (response.ok) {
            const updatedAnimal = await response.json();
            dispatch(updateAnimal(updatedAnimal));
            return updatedAnimal; 
        } else {
            const errorMessage = await response.json();
            return { errors: errorMessage };
        }
    } catch (error) {
        console.error('Error occurred updating the animal:', error);
        return { errors: 'An unexpected error has occurred' };
    }
};

// DELETE A ANIMAL FROM ADOPTION LIST
export const fetchDeleteAnimal = (id) => async (dispatch) => {
    try {
        const response = await fetch(`/api/adoptions/${id}`, {
            method: 'DELETE',
        });
        if (response.ok) {
            dispatch(deleteAnimal(id));
            return { messages: 'Animal deleted successfully!' };
        } else {
            const errorMessages = await response.json();
            return { errors: errorMessages };
        }
    } catch (error) {
        console.error('Error deleting animal from adoption list:', error);
        return { errors: 'An unexpected error has occurred' };
    }
};

const initialState = {
    AllAnimals: [],
    SelectedAnimal: {},
};

function adoptionReducer(state = initialState, action) {
    switch (action.type) {
        case GET_ALL_ANIMALS:
            return { ...state, AllAnimals: action.payload };
        case GET_A_ANIMAL:
            return { ...state, SelectedAnimal: action.paylaod };
        case CREATE_NEW_ANIMAL:
            return { ...state, AllAnimals: [...state.AllAnimals, action.payload] };
        case UPDATE_ANIMAL:
            return {
                ...state, 
                AllAnimals: state.AllAnimals.map((adoption) => adoption.id === action.payload.id ? action.payload : adoption),
                SelectedAnimal: state.SelectedAnimal.id === action.payload.id ? action.payload : state.SelectedAnimal,
            };
        case DELETE_ANIMAL:
            return {
                ...state, 
                AllAnimals: state.AllAnimals.filter(
                    (adoption) => adoption.id === action.payload ? {} : state.SelectedAnimal,
                )
            };
        case CLEAR_SELECTED:
            return { ...state, SelectedAnimal: {} };
        default:
            return state;
    }
};

export default adoptionReducer;