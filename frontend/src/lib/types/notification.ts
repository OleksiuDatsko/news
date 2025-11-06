export interface INotification {
	id: number;
	user_id: number;
	article_id: number | null;
	type: string;
	title: string | null;
	message: string | null;
	is_read: boolean;
	created_at: string;
}
