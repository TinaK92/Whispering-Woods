
// Action Types
export const FETCH_COLORS_REQUEST = 'FETCH_COLORS_REQUEST';
export const FETCH_COLORS_SUCCESS = 'FETCH_COLORS_SUCCESS';
export const FETCH_COLORS_FAILURE = 'FETCH_COLORS_FAILURE';
export const ADD_COLOR_REQUEST = 'ADD_COLOR_REQUEST';
export const ADD_COLOR_SUCCESS = 'ADD_COLOR_SUCCESS';
export const ADD_COLOR_FAILURE = 'ADD_COLOR_FAILURE';
// Action Creators
export const fetchColorsRequest = () => {
    return {
        type: FETCH_COLORS_REQUEST,
    }
};

export const fetchColorsSuccess = (colors) => {
    return {
        type: FETCH_COLORS_SUCCESS,
        payload: colors,
    }
}

export const fetchColorsFailure = (error) => {
    return {
        type: FETCH_COLORS_FAILURE,
        payload: error,
    }
}

export const addColorRequest = () => {
    return {
        type: ADD_COLOR_REQUEST,
    };
};

export const addColorSuccess = (color) => {
    return {
        type: ADD_COLOR_SUCCESS,
        payload: color,
    };
};

export const addColorFailure = (error) => {
    return {
        type: ADD_COLOR_FAILURE,
        payload: error,
    };
};

// Thunks
export const fetchAllColors = () => async (dispatch) => {
    dispatch(fetchColorsRequest());
    try {
        const response = await fetch(`/api/colors`);

        if (!response.ok) {
            throw new Error("Failed to fetch colors")
        }

        const data = await response.json();
        dispatch(fetchColorsSuccess(data.colors));
    } catch (error) {
        dispatch(fetchColorsFailure(error.message));
    }
};

export const addNewColor = (color) => async (dispatch) => {
    dispatch({ type: 'ADD_COLOR_REQUEST' });
    try {
        const response = await fetch('/api/colors/new', { // Updated endpoint
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(color),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to add color');
        }

        const data = await response.json();
        dispatch({ type: 'ADD_COLOR_SUCCESS', payload: data });
        return data;
    } catch (error) {
        dispatch({ type: 'ADD_COLOR_FAILURE', payload: error.message });
        throw error;
    }
};

// Initial State
const initialState = {
    loading: false,
    colors: [],
    error: null,
}

// Reducer 
const colorsReducer = (state = initialState, action) => {
    switch (action.type) {
        case FETCH_COLORS_REQUEST:
            return {
                ...state,
                loading: true,
                error: null,
            };
        case FETCH_COLORS_SUCCESS:
            return {
                ...state,
                loading: false,
                colors: action.payload,
            };
        case FETCH_COLORS_FAILURE:
            return {
                ...state,
                loading: false,
                error: action.payload,
            };
        case ADD_COLOR_REQUEST:
            return {
                ...state,
                loading: true,
            };
        case ADD_COLOR_SUCCESS:
            return {
                ...state,
                loading: false,
                colors: [...state.colors, action.payload], // Add new color to state
            };
        case ADD_COLOR_FAILURE:
            return {
                ...state,
                loading: false,
                error: action.payload,
            };
        default:
            return state;
    }
};

export default colorsReducer;