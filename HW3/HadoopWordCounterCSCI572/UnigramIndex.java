import java.io.IOException;
import java.util.StringTokenizer;
import java.util.HashMap;
import java.util.Map;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;

import org.apache.hadoop.io.Text;

import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class UnigramIndex {
  public static class UnigramMapper extends Mapper<Object, Text, Text, Text> {
    private final static Text docID = new Text();
    private Text word = new Text();

    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
      String seperateTabText[] = value.toString().split("\t", 2);
      docID.set(seperateTabText[0]);
      StringTokenizer itr = new StringTokenizer(seperateTabText[1].toLowerCase().replaceAll("[^a-z]+", " "));
      while (itr.hasMoreTokens()) {
        word.set(itr.nextToken());
        context.write(word, docID);
      }
    }
  }

  public static class UnigramReducer extends Reducer<Text, Text, Text, Text> {
    private Text result = new Text();

    public void reduce(Text key, Iterable<Text> values, Context context)
        throws IOException, InterruptedException {
      // int sum = 0;
      HashMap<String, Integer> counter = new HashMap<String, Integer>();
      for (Text val : values) {
        String docID = val.toString();
        if (counter.containsKey(docID)) {
          counter.put(docID, counter.get(docID) + 1);
        } else {
          counter.put(docID, 1);
        }
      }
      String formatOutput = "";
      for (Map.Entry<String, Integer> e : counter.entrySet()) {
        formatOutput = formatOutput + e.getKey() + ":" + e.getValue() + " ";
      }
      result.set(formatOutput);
      context.write(key, result);
    }
  }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "word count");

    job.setJarByClass(UnigramIndex.class);
    job.setMapperClass(UnigramMapper.class);
    // job.setCombinerClass(IntSumReducer.class);
    job.setReducerClass(UnigramReducer.class);

    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Text.class);

    FileInputFormat.addInputPath(job, new Path(args[0] + "/fulldata"));
    FileOutputFormat.setOutputPath(job, new Path(args[1] + "/UnigramOutput"));

    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}// WordCount
