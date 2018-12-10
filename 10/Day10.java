package com.simon816.aoc;

import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

import javax.imageio.ImageIO;

public class Day10 {

	public static void main(String[] args) throws IOException {
		try (BufferedReader reader = Files.newBufferedReader(Paths.get("../../data/10/output"))) {
			String line;
			int count = 0;
			int t = 0;
			List<boolean[]> points = new ArrayList<>();
			while ((line = reader.readLine()) != null) {
				if (line.isEmpty() || line.charAt(0) == 't') {
					if (!line.isEmpty()) {
						t = Integer.parseInt(line.substring(4));
					}
					if (!points.isEmpty()) {
						BufferedImage img = draw(points);
						ImageIO.write(img, "png", new File("../../data/10/img_" + count + ".png"));
						points = new ArrayList<>();
						count += 1;
						System.out.println("count: " + count + " t: " + t);
					}
					continue;
				}
				boolean[] p = new boolean[line.length()];
				for (int i = 0, len = line.length(); i < len; i++) {
					p[i] = line.charAt(i) == '.' ? false : true;
				}
				points.add(p);
			}
		} finally {
		}
	}

	private static BufferedImage draw(List<boolean[]> points) {
		BufferedImage img = new BufferedImage(points.get(0).length, points.size(), BufferedImage.TYPE_INT_RGB);
		for (int y = 0; y < points.size(); y++) {
			boolean[] line = points.get(y);
			for (int x = 0; x < line.length; x++) {
				boolean b = line[x];
				img.setRGB(x, y, b ? 0 : 0x00FFFFFF);
			}
		}
		return img;
	}

}
