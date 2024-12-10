import 'dotenv/config'
import express from 'express'
import cors from 'cors'
import examsRouter from '../routes/exams'

console.log('Supabase URL:', process.env.SUPABASE_URL)
console.log('Supabase Anon Key:', process.env.SUPABASE_ANON_KEY)

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.use('/exams', examsRouter);

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
