import { useEffect } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { ModalProvider, Modal } from '../context/Modal';
import { thunkAuthenticate } from '../redux/session';
import Navigation from '../components/Navigation/Navigation';

export default function Layout() {
	const dispatch = useDispatch();
	useEffect(() => {
		dispatch(thunkAuthenticate());
	}, [dispatch]);

	return (
		<>
			<ModalProvider>
				<Navigation />
				{<Outlet />}
				<Modal />
			</ModalProvider>
		</>
	);
}
