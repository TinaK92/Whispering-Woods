import { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import {
  fetchCart,
  fetchDeleteItemFromCart,
  fetchClearCart,
} from "../../redux/shoppingCart";
import { useNavigate } from "react-router-dom";

export const ShoppingCart = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const cart = useSelector((state) => state.shoppingCart);
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
    return cart.cart_items
      .reduce((total, item) => {
        return total + item.listing.base_price * item.quantity;
      }, 0)
      .toFixed(2);
  };

  const handleCheckout = () => {
    dispatch(fetchClearCart());
  };

  const handleContinueShopping = () => {
    navigate(`/listings`)
  }

  return (
    <div>
      <div className="shopping-cart">
        <h1>Shopping Cart</h1>
        {cart && cart.cart_items.length > 0 ? (
            <>
                {cart.cart_items.map((item) => (
                    <div
                        key={item.id}
                        classname='cart-item'
                    >
                        <img 
                            className="shop-cart-image"
                            src={item.listing.image_url}
                            alt={item.listing.title
                            }
                        />
                        <div className="cart-info">
                            <div className="cart-item-info">
                                <h3>{item.listing.name}</h3>
                                <p>Price: ${item.listing.base_price}</p>
                            </div>
                            <div className="cart-item-quantity">
                                <button 
                                    classname="cart-quantity-button"
                                    onClick={() => handleUpdateQuantity(item.od, item.quantity + 1)
                                    }
                                    >
                                        +
                                </button>
                                <p>{item.quantity}</p>
                                <button 
                                    className="cart-quantity-button"
                                    onClick={() => handleUpdateQuantity(item.id, item.quantity - 1)
                                    }
                                >
                                    -
                                </button>
                            </div>
                            <button 
                                className="delete-item-button"
                                onClick={() => handleDeleteItem(item.id)
                                }
                                >
                                    Delete
                                </button>
                        </div>
                    </div>
                ))}
                <div className="total">
                    <h3 className="total-price">Total: ${calculateTotal()}</h3>
                </div>
                {cart.cart_items.length > 0 && (
                    <button 
                        className="checkout-button"
                        onClick={handleCheckout}
                    >Checkout</button>
                )}
            </>
        ): (
            <div>
                <p>Your cart is empty.</p>
                <button type='submit' onClick={handleContinueShopping()}>
                    Continue Shopping
                </button>
            </div>
        )}
      </div>
    </div>
  );
};

export default ShoppingCart;
