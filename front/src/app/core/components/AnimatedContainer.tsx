import { motion } from 'framer-motion';

export const AnimatedContainer = ({ children }: { children: React.ReactNode }) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1 }}
      className="container mx-auto p-6"
    >
      {children}
    </motion.div>
  );
};