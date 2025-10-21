export interface IAuthor {
	id: number;
	first_name: string;
	last_name: string;
	bio: string | null;
	articles_count?: number;
}