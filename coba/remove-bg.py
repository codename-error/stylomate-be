import requests

def download_image(url, save_path):
    try:
        # Kirim permintaan GET ke URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Periksa apakah permintaan berhasil

        # Simpan gambar ke file
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print(f"Gambar berhasil diunduh dan disimpan di: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan saat mengunduh gambar: {e}")

# URL gambar Instagram
image_url = "https://instagram.fbdo10-1.fna.fbcdn.net/v/t51.2885-15/489829982_18455282062075593_971224471189671111_n.jpg?stp=dst-jpg_e15_fr_p1080x1080_tt6&_nc_ht=instagram.fbdo10-1.fna.fbcdn.net&_nc_cat=109&_nc_oc=Q6cZ2QERYcz2PCWQhtclpmfCKksv_gi2r2z1gIiX1Z1o1lG-xtgZicR2_jkGkWbyHv4n6gc&_nc_ohc=T-GU9DGe8WQQ7kNvwH7v8LF&_nc_gid=gik7nbM_YfL5sS9qEG1BKw&edm=ANTKIIoBAAAA&ccb=7-5&oh=00_AfEcZN1ktPG74y5-ijHqe3UbGUli6Ro8ZBqUwmdFHUTu6g&oe=681AF254&_nc_sid=d885a2"

# Lokasi penyimpanan file
save_path = "instagram_image.jpg"

# Unduh gambar
download_image(image_url, save_path)