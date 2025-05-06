import { motion } from 'framer-motion';
import { FaHome, FaSignInAlt, FaSignOutAlt } from 'react-icons/fa';

const Navbar = () => {
  return (
    <motion.nav
      className="bg-blue-500 p-4 shadow-md"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1 }}
    >
      <div className="flex justify-between items-center">
        <div className="text-white text-lg font-bold">MangaVerse</div>
        <div className="flex space-x-4">
          <a href="#" className="text-white">
            <FaHome size={20} />
          </a>
          <a href="#" className="text-white">
            <FaSignInAlt size={20} />
          </a>
          <a href="#" className="text-white">
            <FaSignOutAlt size={20} />
          </a>
        </div>
      </div>
    </motion.nav>
  );
};

export default Navbar;