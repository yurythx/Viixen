import { motion } from 'framer-motion';

const Footer = () => {
  return (
    <motion.footer
      className="bg-gray-800 text-white p-4 mt-10"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1 }}
    >
      <div className="text-center">
        &copy; 2025 MangaVerse. Todos os direitos reservados.
      </div>
    </motion.footer>
  );
};

export default Footer;