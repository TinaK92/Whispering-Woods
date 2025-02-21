
// Action Types
export const FETCH_SIZES_REQUEST = 'FETCH_SIZES_REQUEST';
export const FETCH_SIZES_SUCCESS = 'FETCH_SIZES_SUCCESS';
export const FETCH_SIZES_FAILURE = 'FETCH_SIZES_FAILURE';

// Action Creators
export const fetchSizesRequest = () => {
    return {
        type: FETCH_SIZES_REQUEST,
    }
};

export const fetchSizesSuccess = (sizes) => {
    return {
        type: FETCH_SIZES_SUCCESS,
        payload: sizes,
    }
}

export const fetchSizesFailure = (error) => {
    return {
        type: FETCH_SIZES_FAILURE,
        payload: error,
    }
}

// Thunks
export const fetchAllSizes = () => async (dispatch) => {
    dispatch(fetchSizesRequest());
    try {
        const response = await fetch(`/api/sizes`);

        if (!response.ok) {
            throw new Error("Failed to fetch sizes")
        }

        const data = await response.json();
        dispatch(fetchSizesSuccess(data.sizes));
    } catch (error) {
        dispatch(fetchSizesFailure(error.message));
    }
};

// Initial State
const initialState = {
    loading: false,
    sizes: [],
    error: null,
}

// Reducer 
const sizesReducer = (state=initialState, action) => {
    switch (action.type) {
        case FETCH_SIZES_REQUEST:
            return {
                ...state,
                loading: true,
                error: null,
            }
        case FETCH_SIZES_SUCCESS:
            return {
                ...state,
                loading: false,
                sizes: action.payload,
            }
        case FETCH_SIZES_FAILURE:
            return {
                ...state,
                loading: false,
                error: action.payload,
            }
        default:
            return state
    }
}

export default sizesReducer;