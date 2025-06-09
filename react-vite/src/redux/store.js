import {
  legacy_createStore as createStore,
  applyMiddleware,
  compose,
  combineReducers,
} from "redux";
import thunk from "redux-thunk";
import sessionReducer from "./session";
import listingsReducer from "./listing";
import sizesReducer from "./size";
import colorsReducer from "./color";
import adoptionReducer from "./adoption";
import cartReducer from "./shoppingCart";


const rootReducer = combineReducers({
  session: sessionReducer,
  listings: listingsReducer,
  sizes: sizesReducer,
  colors: colorsReducer,
  adoptions: adoptionReducer,
  shoppingCart: cartReducer,
});

let enhancer;
if (import.meta.env.MODE === "production") {
  enhancer = applyMiddleware(thunk);
} else {
  const logger = (await import("redux-logger")).default;
  const composeEnhancers =
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
  enhancer = composeEnhancers(applyMiddleware(thunk, logger));
}

const configureStore = (preloadedState) => {
  return createStore(rootReducer, preloadedState, enhancer);
};

export default configureStore;
