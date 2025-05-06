import { motion } from 'framer-motion';
import { FaBookmark, FaSearch, FaUserAlt } from 'react-icons/fa';

const Sidebar = () => {
  return (
    <motion.div
      className="w-64 bg-gray-800 text-white h-screen p-4"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1 }}
    >
      <div className="space-y-6">
        <div className="flex items-center space-x-2">
          <FaBookmark size={20} />
          <span>Favoritos</span>
        </div>
        <div className="flex items-center space-x-2">
          <FaSearch size={20} />
          <span>Procurar</span>
        </div>
        <div className="flex items-center space-x-2">
          <FaUserAlt size={20} />
          <span>Perfil</span>
        </div>
      </div>
    </motion.div>
  );
};

export default Sidebar;