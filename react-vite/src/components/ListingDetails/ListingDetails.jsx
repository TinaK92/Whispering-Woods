import { useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { fetchGetListing, fetchDeleteListing } from "../../redux/listing";
import { fetchAddToCart } from "../../redux/shoppingCart";


export const ListingDetails = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { id } = useParams();
    const user = useSelector((state) => state.session.user);
    const listing = useSelector((state) => state.listings.selectedListing);

    useEffect(() => {
        dispatch(fetchGetListing(id));
    }, [dispatch, id]);

    if (!listing) {
        return <p>Listing not found!</p>
    }

    const isAdmin = user?.role === "admin";

    const handleEdit = (id) => {
        navigate(`/listings/${id}/edit`)
    };

    const handleDelete = (id) => {
        dispatch(fetchDeleteListing(id));
        navigate('/listings')
    }

    const handleAddToCart = (listing) => {
        dispatch(fetchAddToCart(listing.id))
    }

    return (
        <div className="listing-details-div">
            <img 
                src={`${listing.front_image}`}
                alt={`${listing.name}`}
                className="listing-details-poster"
            />
            <h3 className="listing-name">{listing.name}</h3>
            <p className="listing-description">{listing.description}</p>
            <p className="listing-price">${listing.base_price}</p>
            <p className="listing-color">{listing.color}</p>
            <p className="listing-quantity">In Stock: {listing.quantity}</p>
            <div className="cart-button">
                <button
                    onClick={() => handleAddToCart(listing)}
                >Add To Cart
                </button>
            </div>
            <div className="buttons-div">
                <button
                    onClick={() => handleEdit(listing.id)}
                >Edit Item</button>
                <button
                    onClick={() => handleDelete(listing.id)}
                >Delete Item</button>
            </div>

        </div>
    )
}

export default ListingDetails;