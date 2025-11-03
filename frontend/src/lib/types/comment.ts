export interface IComment {
	id: number;
	article_id: number;
	user: {
		id: number;
		username: string;
	} | null;
	text: string;
	status: string;
	created_at: string;
}