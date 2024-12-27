// Action Types
const GET_ALL_LISTINGS = "listings/GET_ALL_LISTINGS";
const GET_A_LISTING = "listings/GET_A_LISTING";
const CREATE_NEW_LISTING = "listings/CREATE_NEW_LISTING";
const UPDATE_LISTING = "listings/UPDATE_LISTING";
const DELETE_LISTING = "listings/DELETE_LISTING";
const CLEAR_SELECTED = "listings/CLEAR_SELECTED";

// Action Creators
export const getAllListings = (listings) => {
  return {
    type: GET_ALL_LISTINGS,
    payload: listings,
  };
};
export const getAListing = (listing) => {
  return {
    type: GET_A_LISTING,
    payload: listing,
  };
};

export const createNewListing = (listing) => {
  return {
    type: CREATE_NEW_LISTING,
    payload: listing,
  };
};

export const updateListing = (listing) => {
  return {
    type: UPDATE_LISTING,
    payload: listing,
  };
};

export const deleteListing = (listingId) => {
  return {
    type: DELETE_LISTING,
    payload: listingId,
  };
};

export const clearSelected = () => {
  return {
    type: CLEAR_SELECTED,
  };
};

// THUNKS

// Get All Listings
export const fetchAllListings = () => async (dispatch) => {
  const response = await fetch(`/api/listings`);
  if (response.ok) {
    const listings = await response.json();
    dispatch(getAllListings(listings));
    return listings;
  }
};

// Get A Listing
export const fetchGetListing = (id) => async (dispatch) => {
  const response = await fetch(`/api/listings/${id}`);
  if (response.ok) {
    const listing = await response.json();
    dispatch(getAListing(listing));
    return listing;
  }
};

// Create A New Listing
export const fetchCreateListing = (formData) => async (dispatch) => {
  try {
    const response = await fetch(`/api/listings/new`, {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const newListing = await response.json();
      dispatch(createNewListing(newListing));
      return newListing;
    } else {
      const errorMessage = await response.json();
      return { errors: errorMessage };
    }
  } catch (error) {
    console.error(
      "An error has occurred while submitting the new listing:",
      error
    );
    return { errors: "An unexpected error has occurred" };
  }
};

// Update A Listing
export const fetchUpdateListing = (id, formData) => async (dispatch) => {
  try {
    const response = await fetch(`/api/listings/${id}/edit`, {
      method: "PUT",
      body: formData,
    });

    if (response.ok) {
      const updatedListing = await response.json();
      dispatch(updateListing(updatedListing));
      return updatedListing;
    } else {
      const errorMessage = await response.json();
      return { errors: errorMessage };
    }
  } catch (error) {
    console.error("An error occurred while updating the listing:", error);
    return { errors: "An unexpected error has occurred" };
  }
};

// Delete A Listing
export const fetchDeleteListing = (id) => async (dispatch) => {
  try {
    const response = await fetch(`/api/listings/${id}`, {
      method: "DELETE",
    });

    if (response.ok) {
      dispatch(deleteListing(id));
      return { message: "The listing was successfully deleted" };
    } else {
      const errorMessage = await response.json();
      return { errors: errorMessage };
    }
  } catch (error) {
    console.error("An error occurred while deleting the listing:", error);
    return { errors: "An unexpected error has occurred" };
  }
};

// State
const initialState = {
  AllListings: [],
  selectedListing: {},
};

function listingsReducer(state = initialState, action) {
  switch (action.type) {
    case GET_ALL_LISTINGS:
      return { ...state, AllListings: action.payload };
    case GET_A_LISTING:
      return { ...state, selectedListing: action.payload };
    case CREATE_NEW_LISTING:
      return { ...state, AllListings: [...state.AllListings, action.payload] };
    case UPDATE_LISTING:
      return {
        ...state,
        AllListings: state.AllListings.map((listing) =>
          listing.id === action.payload.id ? action.payload : listing
        ),
        selectedListing:
          state.selectedListing.id === action.payload.id
            ? action.payload
            : state.selectedListing,
      };
    case DELETE_LISTING:
      return {
        ...state,
        AllListings: state.AllListings.filter(
          (listing) => listing.id !== action.payload
        ),
        selectedListing:
          state.selectedListing.id === action.payload
            ? {}
            : state.selectedListing,
      };
    case CLEAR_SELECTED:
      return { ...state, selectedListing: {} };
    default:
      return state;
  }
}

export default listingsReducer;
