import { createClient } from '@supabase/supabase-js'

export interface Env {
  SUPABASE_URL: string;
  SUPABASE_SERVICE_KEY: string;
}

export default {
	async fetch(request: Request, env: Env): Promise<Response> {
	  const url = new URL(request.url)
  
	  // Handle CORS preflight (OPTIONS) request
	  if (request.method === 'OPTIONS') {
		return new Response(null, {
		  status: 204,
		  headers: {
			'Access-Control-Allow-Origin': 'https://uiteksamen.pages.dev', 
			'Access-Control-Allow-Methods': 'GET,OPTIONS',
			'Access-Control-Allow-Headers': 'Content-Type',
		  },
		})
	  }
  
	  if (url.pathname === '/exams' && request.method === 'GET') {
		const course_code = url.searchParams.get('course_code')
		
		const supabase = createClient(env.SUPABASE_URL, env.SUPABASE_SERVICE_KEY)
		let query = supabase.from('Exams').select('*')
		
		if (course_code) {
		  query = query.ilike('course_code', `%${course_code}%`)
		}
  
		const { data, error } = await query
		if (error) {
		  return new Response(JSON.stringify({ error: error.message }), {
			status: 500,
			headers: {
			  'Content-Type': 'application/json',
			  'Access-Control-Allow-Origin': 'https://uiteksamen.pages.dev',
			},
		  })
		}
  
		return new Response(JSON.stringify(data || []), {
		  status: 200,
		  headers: {
			'Content-Type': 'application/json',
			'Access-Control-Allow-Origin': 'https://uiteksamen.pages.dev',
		  },
		})
	  }
  
	  // For any other requests, return a 404 with CORS headers as well
	  return new Response(JSON.stringify({ message: 'Not Found' }), {
		status: 404,
		headers: {
		  'Content-Type': 'application/json',
		  'Access-Control-Allow-Origin': 'https://uiteksamen.pages.dev',
		},
	  })
	},
  }
  