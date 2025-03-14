import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchCart } from '../../redux/shoppingCart';
import { useModal } from '../../context/Modal';
import {
	fetchUpdateCartItem,
	fetchDeleteItemFromCart,
	fetchClearCart,
} from '../../redux/shoppingCart';

export const ShoppingCart = () => {
    const dispatch = useDispatch();
    const cart = useSelector((state) => state.cart.cart);
    const user = useSelector((state) => state.session.user);


    useEffect(() => {
        if (user) {
            dispatch(fetchCart(user.id));
        }
    }, [dispatch, user]);

    const handleUpdateQuantity = (itemId, quantity) => {
        if (quantity < 1) {
            dispatch(fetchDeleteItemFromCart(itemId));
        } else {
            dispatch(fetchUpdateCartItem(itemId, quantity));
        }
    };

    const handleDeleteItem = (itemId) => {
        dispatch(fetchDeleteItemFromCart(itemId));
    };

    const calculateTotal = () => {
        return cart.cart_items.reduce((total, item) => {
            return total + item.listing.base_price * item.quantity;
        }, 0).toFixed(2);
    };

    const handleTotal = () => {
        return cart.cart_items.reduce((total, item) => {
            
        })
    }
}